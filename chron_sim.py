# Engine of the software: Chronological simulation of the Hybrid System
import numpy as np
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import smart.kinetic_battery as kb
import smart.synth_solar as synth_solar
import smart.load_model as load_model
import smart.globals as globals

def run_sim(sys_dict, pv_dict, batt_dict, gen_dict, wind_dict):
    latitude = str(globals.latitude)
    longitude = str(globals.longitude)
    hub_height = wind_dict['hub_height']
    wind_point = 50
    if hub_height < 25:
        wind_point = 10
    # Obtains renewable energy resources from the NASA database    
    GHI, Velocity = synth_solar.getResources(globals.start_date, globals.end_date, latitude, longitude, str(wind_point)) 
    hours_in_day = 24.0
    # Initialise simulation output dictionary
    sim_out = {
        'topo'          : '',           # Hybrid system topology
        'P_ld'          : 0,            # Load demand (in kWh/day)
        'G0'            : [],           # GHI (daily in kWh/m2/day)
        'speed'         : [],           # Wind Speed at 50 Meters (m/s)
        'P_pv'          : 0,            # Total PV array output 
        'P_wind'        : 0,            # Total Wind Energy output
        'batt_power'    : 0,            # Remaining battery power in W
        'batt_hours'    : 0,            # How long battery is charged
        'P_gen'         : 0,            # Total generator power used over duration
        'P_gen_xs'      : 0,            # Excess generator output after serving load
        'P_uns'         : 0,            # Power unsupplied  in W
        'P_pv_exc'      : 0,            # Excess solar energy in W
        'opt_area'      : 0,            # New Area of PV required given the percentage of the supply need from PV
        'wind_area'     : 0,             # Recommended Wind Turbine area 
        'opt_wh'        : 0,             # Recommended battery hours
        'opt_gen'       : 0              # Recommended generator size in kW
    }
    
    
    #Update Global Variables
    sim_out['P_ld'] = float(globals.load_kwhd)
    load_Watts = sim_out['P_ld']*(1000.0/24.0)

    # Optimizer Variables
    P_pv_opt = (float(load_Watts) * float(globals.opt_solar))/100.0
    P_wind_opt = (float(load_Watts) * float(globals.opt_wind))/100.0
    P_batt_opt = (float(load_Watts) * float(globals.opt_batt))/100.0
    P_gen_opt = (float(load_Watts) * float(globals.opt_gen))/100.0


    # Unpack system design data dictionary
    is_pv = sys_dict['is_pv']
    is_batt = sys_dict['is_batt']
    is_gen = sys_dict['is_gen']
    is_wind = sys_dict['is_wind']
    lat = sys_dict['lat']

    
    # Unpack PV system data dictionary
    area = pv_dict['area']
    P_coeff = pv_dict['P_coeff']
    PV_eff = pv_dict['PV_eff']
    wire_eff = pv_dict['wire_eff']
    tilt = pv_dict['tilt']
    eff_inv = pv_dict['eff_inv']      
    sim_out['G0'] = GHI
        

    # Unpack Wind system data dictionary
    swept_area = wind_dict['area']
    P_eff = wind_dict['P_eff']
    rho = wind_dict['air_density']
    sim_out['speed'] = Velocity

        
    # Unpack generator data dictionary
    n_gen = gen_dict['n_gen']
    P_gen_rtd = gen_dict['P_gen']
    l_min = gen_dict['l_min']
    e_f = gen_dict['e_f']
    chg_eff = gen_dict['chg_eff']
    c_f = gen_dict['c_f']
    Gen_max_Power = n_gen * P_gen_rtd * 1000           # Maximum generator capacity (in W)
    Gen_min_Power = n_gen * l_min * P_gen_rtd * 1000   # Minimum generator loading (in W)
    sim_out['P_gen_xs'] = Gen_max_Power - Gen_min_Power


    # Unpack battery system data dictionary
    n_batt = batt_dict['n_batt']
    v_n = batt_dict['v_dc']
    C_nom = batt_dict['C_nom']
    SOC_min = batt_dict['SOC_min']
    SOC_cyc = batt_dict['SOC_cyc']
    SOC_0 = batt_dict['SOC_0']
    eff_conv = batt_dict['eff_conv']
    p_set = batt_dict['p_set']
    max_batt_wh = n_batt*v_n*C_nom
    min_batt_wh = SOC_min*n_batt*v_n*C_nom
    batt_charge_wh = (SOC_0*n_batt*v_n*C_nom)/100.0
    print(max_batt_wh)
    print(batt_charge_wh)
        
    # Chronological Simulation
    
    ###########################
    # Generator only topology #
    ###########################
    if is_gen and not is_pv and not is_batt and not is_wind:    
        sim_out['topo'] = (0, 'Generator only')
        #Excess power in watts after serving the primary load
        xs_Power_Watts = 0
        # Total Energy Demand in Watts
        total_demand = load_Watts * (globals.duration+1)
        # Remaining Generator Power after Serving Load
        Gen_Power_Remainder = Gen_max_Power - total_demand
        # Generator Cannot Meet Load
        if Gen_Power_Remainder < Gen_min_Power:
            globals.enough_power = False
            sim_out['P_uns'] = abs(Gen_Power_Remainder) - Gen_min_Power
        else: 
            sim_out['P_gen_xs'] = abs(Gen_Power_Remainder) - Gen_min_Power
            sim_out['P_uns'] = 0
        sim_out['P_gen'] = Gen_max_Power - Gen_min_Power
        
    
    
    #########################
    # PV-Generator topology #
    #########################
    elif is_gen and is_pv and not is_batt and not is_wind:
        sim_out['topo'] = (1, 'Solar PV and Generator')
        #Excess power in watts after serving the primary load
        xs_Power_Watts = 0
        #Total energy from the PV for the given duration
        PV_total = 0
        #Stepping through each daily radiation in the GHI (kW-hr/m^2/day)
        for radiation in GHI:
            # Output power in kWh/d
            PV_out_Kwhd = radiation * pv_dict['area']*pv_dict['PV_eff']*pv_dict['wire_eff']*pv_dict['eff_inv']
            # Total Output PV power in kWh/d
            PV_total = PV_total + PV_out_Kwhd
            # Total Output PV power in Watts
            PV_out_Watts = PV_out_Kwhd*(1000.0/24.0)
            remainder_Watts = PV_out_Watts - load_Watts

            if remainder_Watts > 0:
                xs_Power_Watts = xs_Power_Watts + remainder_Watts

            elif remainder_Watts < 0:
                Gen_Power_Remainder = Gen_max_Power - remainder_Watts
                if Gen_Power_Remainder < Gen_min_Power:
                    globals.enough_power = False
                    sim_out['P_uns'] = abs(Gen_Power_Remainder) - Gen_min_Power

                else: 
                    sim_out['P_gen_xs'] = abs(Gen_Power_Remainder) - Gen_min_Power
                    sim_out['P_uns'] = 0
        sim_out['P_pv'] = PV_total 
        sim_out['P_pv_exc'] = xs_Power_Watts 
        sim_out['P_gen'] = Gen_max_Power - Gen_min_Power
        
     #########################
    # Wind-Generator topology #
    #########################
    elif is_gen and is_wind and not is_batt and not is_pv:
        sim_out['topo'] = (1, 'Wind Turbine and Generator')
        #Excess power in watts after serving the primary load
        xs_Power_Watts = 0
        #Total energy from the PV for the given duration
        PV_total = 0
        for day in Velocity:
            
            wind_out_Watts = 0.5*wind_dict['air_density']*wind_dict['area']*Velocity[day]*Velocity[day]*Velocity[day]*wind_dict['P_eff']
            # Remaining power after supplying the PV power to the load
            remainder_Watts = wind_out_Watts - load_Watts
            # Case 1: The PV met the load need and there is extra PV power
            if remainder_Watts > 0:
                xs_Power_Watts = xs_Power_Watts + remainder_Watts
            # Case 2: PV was unable to meet load. Proceed to Generator
            elif remainder_Watts < 0:
                Gen_Power_Remainder = Gen_max_Power - remainder_Watts
                if Gen_Power_Remainder < Gen_min_Power:
                    globals.enough_power = False
                    sim_out['P_uns'] = abs(Gen_Power_Remainder) - Gen_min_Power

                else: 
                    sim_out['P_gen_xs'] = abs(Gen_Power_Remainder) - Gen_min_Power
                    sim_out['P_uns'] = 0
        sim_out['P_wind'] = Wind_total*(24.0/1000.0) 
        sim_out['P_pv_exc'] = xs_Power_Watts 
        sim_out['P_gen'] = Gen_max_Power - Gen_min_Power
                    
    #######################
    # PV-Battery topology #
    #######################
    elif not is_gen and is_pv and is_batt and not is_wind:
        sim_out['topo'] = (2, 'Solar PV and Battery')
        batt_charge_wh = 0
        #Excess power in watts after serving the primary load
        xs_Power_Watts = 0
        #Total energy from the PV for the given duration
        PV_total = 0
        charge_hours = 0
        #Stepping through each daily radiation in the GHI (kW-hr/m^2/day)
        for radiation in GHI:
            PV_out_Kwhd = radiation * pv_dict['area']*pv_dict['PV_eff']*pv_dict['wire_eff']*pv_dict['eff_inv']
            PV_total = PV_total + PV_out_Kwhd
            PV_out_Watts = PV_out_Kwhd*(1000.0/24.0)
            remainder_Watts = PV_out_Watts - load_Watts
            # Case 1: The PV met the load need and there is extra PV power
            if remainder_Watts > 0:
                # Determining how much energy is needed to fully charge the battery
                needed_Charge_wh = max_batt_wh - batt_charge_wh
                if needed_Charge_wh == 0:
                    xs_Power_Watts = xs_Power_Watts + remainder_Watts
                else: 
                    charge_hours = (needed_Charge_wh/remainder_Watts)
                    batt_charge_wh = max_batt_wh 
            # Case 2: PV was unable to meet load. Proceed to discharging the battery
            elif remainder_Watts < 0:
                batt_charge_Watts = (batt_charge_wh/hours_in_day)
                unmet_load_Watts = abs(remainder_Watts) - batt_charge_Watts
                if unmet_load_Watts < 0:
                    batt_charge_Watts = batt_charge_Watts - abs(remainder_Watts)
                    batt_charge_wh = batt_charge_Watts*hours_in_day
                else: 
                    globals.enough_power = False
                    sim_out['P_uns'] = unmet_load_Watts
        sim_out['P_pv'] = PV_total 
        sim_out['P_pv_exc'] = xs_Power_Watts 
        sim_out['batt_power'] = batt_charge_wh
        sim_out['batt_hours'] = charge_hours

    #######################
    # Wind-Battery topology #
    #######################
    elif not is_gen and is_wind and is_batt and not is_pv:
        sim_out['topo'] = (2, 'Wind Turbine and Battery')
        batt_charge_wh = 0
        #Excess power in watts after serving the primary load
        xs_Power_Watts = 0
        #Total energy from Wind for the given duration
        Wind_total = 0
        charge_hours = 0
        for day in Velocity:
            # Output power in kWh/d
            wind_out_Watts = 0.5*wind_dict['air_density']*wind_dict['area']*Velocity[day]*Velocity[day]*Velocity[day]*wind_dict['P_eff']
            # Remaining power after supplying the Wind power to the load
            remainder_Watts = wind_out_Watts - load_Watts
            # Case 1: The Wind power met the load need and there is extra PV power
            if remainder_Watts > 0:
                # Determining how much energy is needed to fully charge the battery
                needed_Charge_wh = max_batt_wh - batt_charge_wh
                if needed_Charge_wh == 0:
                    xs_Power_Watts = xs_Power_Watts + remainder_Watts
                else: 
                    charge_hours = (needed_Charge_wh/remainder_Watts)
                    batt_charge_wh = max_batt_wh 
            # Case 2: Wind power was unable to meet load. Proceed to discharging the battery
            elif remainder_Watts < 0:
                batt_charge_Watts = (batt_charge_wh/hours_in_day)
                unmet_load_Watts = abs(remainder_Watts) - batt_charge_Watts
                if unmet_load_Watts < 0:
                    batt_charge_Watts = batt_charge_Watts - abs(remainder_Watts)
                    batt_charge_wh = batt_charge_Watts*hours_in_day
                else: 
                    globals.enough_power = False
                    sim_out['P_uns'] = unmet_load_Watts
        sim_out['P_wind'] = Wind_total*(24.0/1000.0)
        sim_out['P_pv_exc'] = xs_Power_Watts 
        sim_out['batt_power'] = batt_charge_wh
        sim_out['batt_hours'] = charge_hours

   
                
    #################################
    # PV-Battery-Generator topology #
    #################################
    elif not is_wind and is_gen and is_pv and is_batt:
        #######################################################################
        sim_out['topo'] = (3, 'Solar PV - Battery - Generator')
        #Excess power in watts after serving the primary load 
        xs_Power_Watts = 0
        #Total energy from the PV for the given duration
        PV_total = 0
        #How long the battery gets charged
        charge_hours = 0
        # The battery charge in Watt Hours
        batt_charge_wh = 0
        #Stepping through each daily radiation in the GHI (kW-hr/m^2/day)
        for radiation in GHI:
            # Output power in kWh/d
            PV_out_Kwhd = radiation * pv_dict['area']*pv_dict['PV_eff']*pv_dict['wire_eff']*pv_dict['eff_inv']
            PV_total = PV_total + PV_out_Kwhd
            # The Output power in Watts
            PV_out_Watts = PV_out_Kwhd*(1000.0/24.0)
            # Remaining power after supplying the PV power to the load
            remainder_Watts = PV_out_Watts - load_Watts
            # Case 1: The PV met the load need and there is extra PV power
            if remainder_Watts > 0:
                # Determining how much energy is needed to fully charge the battery
                needed_Charge_wh = max_batt_wh - batt_charge_wh
                if needed_Charge_wh == 0:
                    xs_Power_Watts = xs_Power_Watts + remainder_Watts
                else: 
                    charge_hours = (needed_Charge_wh/remainder_Watts)
                    # Reset the battery to full charge after charging for charge_hours
                    batt_charge_wh = max_batt_wh 
            # Case 2: PV was unable to meet load. Proceed to discharging the battery
            elif remainder_Watts < 0:
                # Convert the battery energy to power
                batt_charge_Watts = (batt_charge_wh/hours_in_day)
                # Unmet load need after discharging battery
                unmet_load_Watts = abs(remainder_Watts) - batt_charge_Watts
                # Battery was able to meet the power required by the load
                if unmet_load_Watts < 0:
                    # Remaining battery power after the serving the load
                    batt_charge_Watts = batt_charge_Watts - abs(remainder_Watts)
                    # Remaining battery energy after the serving the load
                    batt_charge_wh = batt_charge_Watts * 24.0
                    # Battery unable to serve load, proceed to the garge_Watts*hours_in_day
                else: 
                    Gen_Power_Remainder = Gen_max_Power - unmet_load_Watts
                    if Gen_Power_Remainder < Gen_min_Power:
                        globals.enough_power = False
                        sim_out['P_uns'] = abs(Gen_Power_Remainder) - Gen_min_Power

                    else: 
                        sim_out['P_gen_xs'] = abs(Gen_Power_Remainder) - Gen_min_Power
                        sim_out['P_uns'] = 0
        sim_out['P_pv'] = PV_total 
        sim_out['P_gen'] = Gen_max_Power - Gen_min_Power
        sim_out['P_pv_exc'] = xs_Power_Watts 
        sim_out['batt_power'] = batt_charge_wh
        sim_out['batt_hours'] = charge_hours

    elif not is_pv and is_gen and is_wind and is_batt:
        #######################################################################
        sim_out['topo'] = (3, 'Wind Turbine - Battery - Generator')
        #Excess power in watts after serving the primary load 
        xs_Power_Watts = 0
        #Total energy from Wind for the given duration
        Wind_total = 0
        #How long the battery gets charged
        charge_hours = 0
        # The battery charge in Watt Hours
        batt_charge_wh = 0
        #Stepping through each daily radiation in the GHI (kW-hr/m^2/day)
        for day in Velocity:
            # Output power in kWh/d
            wind_out_Watts = 0.5*wind_dict['air_density']*wind_dict['area']*Velocity[day]*Velocity[day]*Velocity[day]*wind_dict['P_eff']
            # Remaining power after supplying the PV power to the load
            remainder_Watts = wind_out_Watts - load_Watts
            # Case 1: The PV + Wind power met the load need and there is extra PV power
            if remainder_Watts > 0:
                # Determining how much energy is needed to fully charge the battery
                needed_Charge_wh = max_batt_wh - batt_charge_wh
                if needed_Charge_wh == 0:
                    xs_Power_Watts = xs_Power_Watts + remainder_Watts
                else: 
                    charge_hours = (needed_Charge_wh/remainder_Watts)
                    # Reset the battery to full charge after charging for charge_hours
                    batt_charge_wh = max_batt_wh 
            # Case 2: PV was unable to meet load. Proceed to discharging the battery
            elif remainder_Watts < 0:
                # Convert the battery energy to power
                batt_charge_Watts = (batt_charge_wh/hours_in_day)
                # Unmet load need after discharging battery
                unmet_load_Watts = abs(remainder_Watts) - batt_charge_Watts
                # Battery was able to meet the power required by the load
                if unmet_load_Watts < 0:
                    # Remaining battery power after the serving the load
                    batt_charge_Watts = batt_charge_Watts - abs(remainder_Watts)
                    # Remaining battery energy after the serving the load
                    batt_charge_wh = batt_charge_Watts * 24.0
                    # Battery unable to serve load, proceed to the garge_Watts*hours_in_day
                else: 
                    Gen_Power_Remainder = Gen_max_Power - unmet_load_Watts
                    if Gen_Power_Remainder < Gen_min_Power:
                        globals.enough_power = False
                        sim_out['P_uns'] = abs(Gen_Power_Remainder) - Gen_min_Power

                    else: 
                        sim_out['P_gen_xs'] = abs(Gen_Power_Remainder) - Gen_min_Power
                        sim_out['P_uns'] = 0
       
        sim_out['P_gen'] = Gen_max_Power - Gen_min_Power
        sim_out['P_wind'] = Wind_total*(24.0/1000.0)
        sim_out['P_pv_exc'] = xs_Power_Watts
        sim_out['batt_power'] = batt_charge_wh
        sim_out['batt_hours'] = charge_hours



    elif is_gen and is_pv and is_batt and is_wind and not globals.optimizer:
        #######################################################################
        sim_out['topo'] = (3, 'Solar PV - Wind Turbine - Battery - Generator')
        #Excess power in watts after serving the primary load 
        xs_Power_Watts = 0
        #Total energy from the PV for the given duration
        PV_total = 0
        #Total energy from Wind for the given duration
        Wind_total = 0
        #How long the battery gets charged
        charge_hours = 0
        # The battery charge in Watt Hours
        batt_charge_wh = 0
        #Selected Day
        day_i = 0
        #Stepping through each daily radiation in the GHI (kW-hr/m^2/day)
        for radiation in GHI:
            # Output power in kWh/d
            PV_out_Kwhd = radiation * pv_dict['area']*pv_dict['PV_eff']*pv_dict['wire_eff']*pv_dict['eff_inv']
            wind_out_Watts = 0.5*wind_dict['air_density']*wind_dict['area']*Velocity[day_i]*Velocity[day_i]*Velocity[day_i]*wind_dict['P_eff']
            PV_total = PV_total + PV_out_Kwhd
            Wind_total = Wind_total + wind_out_Watts
            # The Output power in Watts
            PV_out_Watts = PV_out_Kwhd*(1000.0/24.0)
            #Total Energy in Watts from summing PV and Wind
            E_total_Watts = PV_out_Watts + wind_out_Watts
            # Remaining power after supplying the PV power to the load
            remainder_Watts = E_total_Watts - load_Watts
            # Case 1: The PV met the load need and there is extra PV power
            if remainder_Watts > 0:
                # Determining how much energy is needed to fully charge the battery
                print('battery fully Charged')
                needed_Charge_wh = max_batt_wh - batt_charge_wh
                if needed_Charge_wh == 0:
                    xs_Power_Watts = xs_Power_Watts + remainder_Watts
                else: 
                    charge_hours = (needed_Charge_wh/remainder_Watts)
                    # Reset the battery to full charge after charging for charge_hours
                    batt_charge_wh = max_batt_wh 
            # Case 2: PV was unable to meet load. Proceed to discharging the battery
            elif remainder_Watts < 0:
                # Convert the battery energy to power
                batt_charge_Watts = (batt_charge_wh/hours_in_day)
                # Unmet load need after discharging battery
                unmet_load_Watts = abs(remainder_Watts) - batt_charge_Watts
                # Battery was able to meet the power required by the load
                if unmet_load_Watts < 0:
                    # Remaining battery power after the serving the load
                    batt_charge_Watts = batt_charge_Watts - abs(remainder_Watts)
                    # Remaining battery energy after the serving the load
                    batt_charge_wh = batt_charge_Watts * 24.0
                    # Battery unable to serve load, proceed to the garge_Watts*hours_in_day
                else: 
                    print('battery fully discharged')
                    Gen_Power_Remainder = Gen_max_Power - unmet_load_Watts
                    if Gen_Power_Remainder < Gen_min_Power:
                        globals.enough_power = False
                        sim_out['P_uns'] = abs(Gen_Power_Remainder) - Gen_min_Power
                        sim_out['P_gen'] = sim_out['P_gen'] + (Gen_max_Power - Gen_min_Power)
                        sim_out['P_gen_xs'] = 0

                    else: 
                        sim_out['P_gen_xs'] = abs(Gen_Power_Remainder) - Gen_min_Power
                        sim_out['P_uns'] = 0
            day_i = day_i + 1
        sim_out['P_pv'] = PV_total 
        sim_out['P_wind'] = Wind_total*(24.0/1000.0)
        sim_out['P_pv_exc'] = xs_Power_Watts 
        sim_out['batt_power'] = batt_charge_wh
        sim_out['batt_hours'] = charge_hours

    elif globals.optimizer == True:
        #######################################################################
        sim_out['topo'] = (3, 'Solar PV - Wind Turbine - Battery - Generator')
        #Excess power in watts after serving the primary load 
        xs_Power_Watts = 0
        #Total energy from the PV for the given duration
        PV_total = 0
        #Total energy from Wind for the given duration
        Wind_total = 0
        #How long the battery gets charged
        charge_hours = 0
        # The battery charge in Watt Hours
        batt_charge_wh = 0
        #Selected Day
        day_i = 0
        #Stepping through each daily radiation in the GHI (kW-hr/m^2/day)
        for radiation in GHI:
            # Output power in kWh/d
            PV_out_Kwhd = radiation * pv_dict['area']*pv_dict['PV_eff']*pv_dict['wire_eff']*pv_dict['eff_inv']
            wind_out_Watts = 0.5*wind_dict['air_density']*wind_dict['area']*Velocity[day_i]*Velocity[day_i]*Velocity[day_i]*wind_dict['P_eff']
            PV_total = PV_total + PV_out_Kwhd
            Wind_total = Wind_total + wind_out_Watts
            # The Output power in Watts
            PV_out_Watts = PV_out_Kwhd*(1000.0/24.0)
            #Total Energy in Watts from summing PV and Wind
            E_total_Watts = PV_out_Watts + wind_out_Watts
            # Remaining power after supplying the PV power to the load
            remainder_Watts = E_total_Watts - load_Watts
            # Case 1: The PV met the load need and there is extra PV power
            if remainder_Watts > 0:
                # Determining how much energy is needed to fully charge the battery
                needed_Charge_wh = max_batt_wh - batt_charge_wh
                if needed_Charge_wh == 0:
                    xs_Power_Watts = xs_Power_Watts + remainder_Watts
                else: 
                    charge_hours = (needed_Charge_wh/remainder_Watts)
                    # Reset the battery to full charge after charging for charge_hours
                    batt_charge_wh = max_batt_wh 
            # Case 2: PV was unable to meet load. Proceed to discharging the battery
            elif remainder_Watts < 0:
                # Convert the battery energy to power
                batt_charge_Watts = (batt_charge_wh/hours_in_day)
                # Unmet load need after discharging battery
                unmet_load_Watts = abs(remainder_Watts) - batt_charge_Watts
                # Battery was able to meet the power required by the load
                if unmet_load_Watts < 0:
                    # Remaining battery power after the serving the load
                    batt_charge_Watts = batt_charge_Watts - abs(remainder_Watts)
                    # Remaining battery energy after the serving the load
                    batt_charge_wh = batt_charge_Watts*24
                    # Battery unable to serve load, proceed to the garge_Watts*hours_in_day
                else: 
                    Gen_Power_Remainder = Gen_max_Power - unmet_load_Watts
                    if Gen_Power_Remainder < Gen_min_Power:
                        globals.enough_power = False
                        sim_out['P_gen_xs'] = 0
                        sim_out['P_gen'] = sim_out['P_gen'] + (Gen_max_Power - Gen_min_Power)
                        sim_out['P_uns'] = abs(Gen_Power_Remainder) - Gen_min_Power

                    else: 
                        sim_out['P_gen_xs'] = abs(Gen_Power_Remainder) - Gen_min_Power
                        sim_out['P_uns'] = 0
            day_i = day_i + 1
        sim_out['P_pv'] = PV_total 
        sim_out['P_wind'] = Wind_total*(24.0/1000.0)
        
        sim_out['P_pv_exc'] = xs_Power_Watts 
        sim_out['batt_power'] = batt_charge_wh
        sim_out['batt_hours'] = charge_hours

        # Autosize Optimizer
        PV_total_watts = PV_total*(1000.0/24.0)
        sim_out['opt_area']  = (P_pv_opt/PV_total_watts)*pv_dict['area']
        sim_out['wind_area'] = (P_wind_opt/Wind_total)*wind_dict['area']
        sim_out['opt_wh']    = P_batt_opt * 24
        sim_out['opt_gen']   = round((P_gen_opt/1000.0), 5)

        
    return sim_out