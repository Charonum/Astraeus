import base64
import os
import pathlib
from st_clickable_images import clickable_images
import numpy
import pandas as pd
import streamlit as st

import utils

main_pth = str(pathlib.Path(__file__).parent.parent.resolve()).replace('\\', '/')

sys_name = open(f"{main_pth}/sys_name.txt", "r").read()

st.subheader("Template Settings")

type_ = st.selectbox("Planet Type",
                     options=["Habitable/Atmospheric (Laythe)", "Mun-Like (Moho)", "Non-Spherical Gilly-Like (Gilly)", "Gas Giant (Jool)", "Custom"])
if type_ == "Custom":
    template = st.text_input("Template:")

st.subheader("Global Settings")
name = st.text_input("Name")
display_name = st.text_input("Display Name")
desc = st.text_area("Description")
cont_weight = st.slider("Contract Weight")
radius = st.number_input("Radius (1 = Radius of Kerbin)")
rotates = st.checkbox("Tidally Locked", value=False)
rotation = st.number_input("Rotation Period (sec)")
color = st.color_picker("Map View Color")

if type_ == "Habitable/Atmospheric (Laythe)":
    st.subheader("Template Specific Settings")
    template = "Laythe"
    ocean = st.checkbox("Has Ocean")
    alb = st.slider("Albedo", min_value=0.0, max_value=1.0, step=0.01)
    emm = st.slider("Emissivity", min_value=0.0, max_value=1.0, step=0.01)
    footprints = st.checkbox("Kerbals Create Footprints?")
elif type_ == "Mun-Like (Moho)":
    template = "Moho"
    footprints = st.checkbox("Kerbals Create Footprints?")
elif type_ == "Non-Spherical Gilly-Like (Gilly)":
    template = "Gilly"
    footprints = st.checkbox("Kerbals Create Footprints?")
elif type_ == "Gas Giant (Jool)":
    st.subheader("Template Specific Settings")
    template = "Jool"
    alb = st.slider("Albedo", min_value=0.0, max_value=1.0, step=0.01)
    emm = st.slider("Emissivity", min_value=0.0, max_value=1.0, step=0.01)
else:
    footprints = st.checkbox("Kerbals Create Footprints?")

st.subheader("Advanced Settings")
with st.expander(
        "Orbiting Info"):
    options = []
    try:
        for i in os.listdir("_" + sys_name + "/_Celestials"):
            if "." not in i:
                for i2 in os.listdir("_" + sys_name + "/_Celestials/" + i):
                    try:
                        options.append(i2.replace(".cfg", "").split("_")[1])
                    except:
                        options.append(i2.replace(".cfg", ""))
            else:
                options.append(i.replace(".cfg", ""))
    except:
        pass
    orb = st.selectbox("Orbiting:", options=options)
    per = st.number_input("Period (in days)")
    inc = st.number_input("Inclination/ Tilt (in degrees)")
    ecc = st.number_input("Eccentricity (0-1)")
    sma = st.number_input("Semi Major Axis (in KAU)")
    loam = st.number_input("Longitude of Ascending Node (in degrees)")
    aop = st.number_input("Argument of Periapsis (in degrees)")
    ma = st.number_input(
        "Mean Anomaly at Epoch (Distance, in degrees, that the planet/moon has travelled past its periapsis)")

with st.expander("Mapping Info"):
    st.info("Random generation coming soon. Check the roadmap at https://github.com/Charonum/Astraeus")
    biome_map = st.file_uploader("Biome Map", accept_multiple_files=False)
    height_map = st.file_uploader("Height Map", accept_multiple_files=False)
    normal_map = st.file_uploader("Normal Map", accept_multiple_files=False)
    color_map = st.file_uploader("Color Map", accept_multiple_files=False)
    if 'biomes' not in st.session_state:
        st.session_state['biomes'] = []
    biome_name = st.text_input("Biome Name")
    biome_color = st.color_picker("Biome Map Color")
    if st.button("➕ Add Biome"):
        st.session_state['biomes'].append(
            [biome_name, biome_color])
        st.experimental_rerun()
    st.table(st.session_state['biomes'])
    if st.button("➖ Remove Biome"):
        st.session_state['biomes'].remove(st.session_state['biomes'][-1])
        st.experimental_rerun()

if template == "Laythe" or template == "Jool":
    with st.expander("Atmosphere Info"):
        st.warning(
            "For the time being, your entries MUST:\n1. Be ordered from least to greatest altitude\n2. Contain an entry (should be the first entry you create) with the altitude of 0 km")
        if 'temp_curve' not in st.session_state:
            st.session_state['temp_curve'] = {}
        if 'psi_curve' not in st.session_state:
            st.session_state['psi_curve'] = {}
        alt = st.number_input("Altitude at given point (km)")
        temp = st.number_input("Temperature at given point (K)")
        psi = st.number_input("Pressure at given point (kPa)")
        if st.button("➕ Add Point"):
            try:
                st.session_state['temp_curve'][alt * 1000] = temp
                st.session_state['psi_curve'][alt * 1000] = psi
            except:
                st.error("You have already set data for this value.")
        st.write(name + " Temperature Curve")
        keys = list(st.session_state['temp_curve'].keys())
        keys.sort()
        user_data = []
        for i in keys:
            user_data.append([i / 1000, st.session_state['temp_curve'].get(i)])
        try:
            temp_df = pd.DataFrame(user_data)
            temp_df.columns = ["Altitude (km)", "Temperature (K)"]
        except:
            pass
        st.table(temp_df)
        st.write(name + " Pressure Curve")
        keys = list(st.session_state['psi_curve'].keys())
        keys.sort()
        psi_user_data = []
        for i in keys:
            psi_user_data.append([i / 1000, st.session_state['psi_curve'].get(i)])
        try:
            psi_df = pd.DataFrame(psi_user_data)
            psi_df.columns = ["Altitude (km)", "Pressure (kPa)"]
        except:
            pass
        st.table(psi_df)
        if st.button("Clear Table Data"):
            st.session_state['temp_curve'].clear()
            st.session_state['psi_curve'].clear()
            st.experimental_rerun()
        st.header("Additional Data")
        oxygen = st.checkbox("Breathable?")
        if st.selectbox("Mode", options=["Simple", "Advanced"]) == "Simple":
            atm_height = st.number_input(
                "Atmosphere Height (km)")
            zero_day = st.number_input("Temperature at 0° Latitude (Day)")
            zero_night = st.number_input("Temperature at 0° Latitude (Night)")
            mid_day = st.number_input("Temperature at 38° Latitude (Day)")
            mid_night = st.number_input("Temperature at 38° Latitude (Night)")
            ninety_day = st.number_input("Temperature at 90° Latitude (Day)")
            ninety_night = st.number_input("Temperature at 90° Latitude (Night)")
            orb_ecc_var = st.number_input("Orbital Eccentricity Variation (total)")
        else:
            def add_remove_buttons(ssid):
                if st.button("Add Row", key=ssid + "."):
                    keys = []
                    st.session_state[ssid].loc[len(st.session_state[ssid].index)] = [0, 0, 0, 0]
                    for _ in st.session_state[ssid].index:
                        keys.append("key =")
                    st.session_state[ssid].index = keys
                    st.experimental_rerun()
                if st.button("Remove Row", key=ssid + ","):
                    keys = []
                    num = 1
                    for _ in st.session_state[ssid].index:
                        keys.append(num)
                        num += 1
                    st.session_state[ssid].index = keys
                    st.session_state[ssid] = st.session_state[ssid].drop(len(st.session_state[ssid].index))
                    keys = []
                    for _ in st.session_state[ssid].index:
                        keys.append("key =")
                    st.session_state[ssid].index = keys
                    st.experimental_rerun()
            st.subheader("Variation by Altitude")

            st.write("temperatureSunMultCurve")
            if "tsmc" not in st.session_state:
                st.session_state["tsmc"] = pd.DataFrame([[0, 0, 0, 0]])
                st.session_state["tsmc"].index = ["key ="]
            st.data_editor(st.session_state["tsmc"], key="tsmc:")
            add_remove_buttons("tsmc")

            st.subheader("Diurnal Variation")

            st.write("temperatureLatitudeSunMultCurve")
            if "tlsmc" not in st.session_state:
                st.session_state["tlsmc"] = pd.DataFrame([[0, 0, 0, 0], [38, 0, 0, 0], [90, 0, 0, 0]])
                st.session_state["tlsmc"].index = ["key =", "key =", "key ="]
            st.data_editor(st.session_state["tlsmc"])
            add_remove_buttons("tlsmc")

            st.write("temperatureLatitudeBiasCurve")
            if "tlbc" not in st.session_state:
                st.session_state["tlbc"] = pd.DataFrame([[0, 0, 0, 0], [38, 0, 0, 0], [90, 0, 0, 0]])
                st.session_state["tlbc"].index = ["key =", "key =", "key ="]
            st.data_editor(st.session_state["tlsmc"], key="tlbc:")
            add_remove_buttons("tlbc")

            st.subheader("Seasonal Variation")

            st.write("temperatureAxialSunMultCurve")
            if "tasmc" not in st.session_state:
                st.session_state["tasmc"] = pd.DataFrame([[0, 0, 0, 0], [90, 0, 0, 0]])
                st.session_state["tasmc"].index = ["key =", "key ="]
            st.data_editor(st.session_state["tasmc"])
            add_remove_buttons("tasmc")

            st.write("temperatureAxialSunBiasCurve")
            if "tabc" not in st.session_state:
                st.session_state["tabc"] = pd.DataFrame([[0, 0, 0, 0], [360, 0, 0, 0]])
                st.session_state["tabc"].index = ["key =", "key ="]
            st.data_editor(st.session_state["tabc"])
            add_remove_buttons("tabc")

            st.subheader("Orbital Eccentricity Variation")

            st.write("temperatureEccentricityBiasCurve")
            if "tebc" not in st.session_state:
                st.session_state["tebc"] = pd.DataFrame([[0, 0, 0, 0], [1, 0, 0, 0]])
                st.session_state["tebc"].index = ["key =", "key ="]
            st.data_editor(st.session_state["tebc"])
            add_remove_buttons("tebc")
        st.write("---")
        st.subheader("Atmosphere Composition")
        moles = {
            'Acetylene, C2H2': 26.038,
            'Air': 28.966,
            'Ammonia (R-717)': 17.02,
            'Argon, Ar': 39.948,
            'Benzene': 78.114,
            'n - Butane, C4H10': 58.124,
            '1,2 - Butadiene': 54.092,
            '1-Butene': 56.108,
            'cis -2-Butene': 56.108,
            'trans-2-Butene': 56.108,
            'Butylene': 56.06,
            'Carbon Dioxide, CO2': 44.01,
            'Carbon Disulphide': 76.13,
            'Carbon Monoxide, CO': 28.011,
            'Chlorine': 70.906,
            'Cyclohexane': 84.162,
            'Cyclopentane': 70.135,
            'n - Decane': 142.286,
            'Deuterium': 2.014,
            '2,3 - Dimetylbutane': 86.178,
            '2,2 - Dimethylpentane': 100.205,
            'Diisobutyl': 114.232,
            'Duoderane': 170.21,
            'Ethane, C2H6': 30.07,
            'Ethene': 28.05,
            'Ethyl Alcohol': 46.07,
            'Ethylbenzene': 106.168,
            'Ethyl Chloride': 64.515,
            '3 - Ethylpentane': 100.205,
            'Ethylene, C2H4': 28.054,
            'Fluorine': 37.996,
            'Helium, He': 4.002602,
            'n - Heptane': 100.205,
            'n - Hexane': 86.178,
            'Hydrochloric Acid': 36.47,
            'Hydrogen, H2': 2.016,
            'Hydrogen Chloride': 36.461,
            'Hydrogen Sulfide': 34.076,
            'Hydroxyl, OH': 17.01,
            'Isobutane (2-Metyl propane)': 58.124,
            'Isobutene': 56.108,
            'Isooctane': 210.63,
            'Isopentane': 72.151,
            'Isoprene': 68.119,
            'Isopropylbenzene': 120.195,
            'Krypton': 83.8,
            'Methane, CH4': 16.043,
            'Methyl Alcohol': 32.04,
            'Methyl Butane': 72.15,
            'Methyl Chloride': 50.488,
            'Methylcyclohexane': 98.189,
            'Methylcyclopentane': 84.162,
            '2 - Methylhexane': 100.205,
            '2 - Methylpentane': 86.178,
            'Natural Gas': 19.0,
            'Neon, Ne': 20.179,
            'Neohexane': 86.178,
            'Neopentane': 72.151,
            'Nitric Oxide, NO': 30.006,
            'Nitrogen, N2': 28.0134,
            'Nitrous Oxide, N2O': 44.013,
            'n - Nonane': 128.259,
            'n - Octane': 114.232,
            'Oxygen, O2': 31.9988,
            'Ozone': 47.998,
            'n - Pentane': 72.151,
            'Pentylene': 70.08,
            'Propane, C3H8': 44.097,
            'Propene': 42.081,
            'Propylene': 42.08,
            'R-11': 137.37,
            'R-12': 120.92,
            'R-22': 86.48,
            'R-114': 170.93,
            'R-123': 152.93,
            'R-134a': 102.03,
            'R-611': 60.05,
            'Styrene': 104.152,
            'Sulfur': 32.02,
            'Sulfur Dioxide (Sulphur Dioxide)': 64.06,
            'Sulfuric Oxide': 48.1,
            'Toluene, toluol': 92.141,
            'Triptane': 100.205,
            'Xenon': 131.3,
            'o - Xylene, xylol': 106.168,
            'Water Vapor - Steam, H2O': 18.02
        }
        st.warning("To prevent issues, molarity values below 0.0001 will not be shown. Contact me if your use case requires this to be changed")
        element_names = []
        for i in moles.keys():
            element_names.append(i)
        element = st.selectbox("Compound", options=element_names)
        ppm = st.number_input("Parts Per Million (ppm)")
        if "mol" not in st.session_state:
            st.session_state["mol"] = pd.DataFrame([["Compound", 0, 0]])
        if st.button("Add Compound"):
            if "Compound" in st.session_state['mol'].values:
                st.session_state["mol"] = st.session_state["mol"].drop(0)
            if element not in st.session_state['mol'].values:
                st.session_state['mol'].loc[len(st.session_state["mol"].index)] = [element, ppm, ppm / moles.get(element) / 1000]
            else:
                st.error("Element already exists in table!")
        st.table(st.session_state['mol'])
        values = []
        for i in st.session_state['mol'].values:
            values.append(i[2])
        molar_mass = round(sum(values), 4)
        st.markdown(f'<p align="right">Total Molar Mass: {molar_mass}</p>', unsafe_allow_html=True)



with st.expander("Texturing Info"):
    st.info("When selecting images, it may take a moment for Astraeus to register what you clicked.")
    files = []
    images = []
    titles = []
    for i in os.listdir("textures"):
        files.append('textures/' + i)
        titles.append(i.replace('.png', ''))
    for file in files:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")
    st.subheader("Steep Texture")
    steep = clickable_images(
        images,
        titles=titles,
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "100px"},
    )
    st.markdown(f"Status: {titles[steep]} selected" if steep > -1 else "Status: No texture selected")
    power = st.slider("Steep Texture Authority/Power", max_value=10)
    st.write("----")
    st.subheader("Ground Level Texture")
    titles.append("a")
    mid = clickable_images(
        images,
        titles=titles,
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "100px"},

    )
    st.markdown(f"Status: {titles[mid]} selected" if mid > -1 else "Status: No texture selected")
    st.write("----")
    st.subheader("Ground Level Bump Map")
    files = []
    images = []
    bump_titles = []
    for i in os.listdir("normals"):
        files.append('normals/' + i)
        bump_titles.append(i.replace('.png', '').replace('MiConv.com__', '')) # MiConv.com is good for .dds to .png. I didn't rename the images
    for file in files:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")
    mid_bump = clickable_images(
        images,
        titles=bump_titles,
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "100px"},

    )
    st.markdown(f"Status: {bump_titles[mid_bump]} selected" if mid_bump > -1 else "Status: No texture selected")
    if template == "Laythe" or template == "Jool":
        st.write("----")
        files = []
        images = []
        ramp_titles = []
        for i in os.listdir("ramps"):
            files.append('ramps/' + i)
            ramp_titles.append(i.replace('_Ramp.png', ''))
        for file in files:
            with open(file, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
                images.append(f"data:image/jpeg;base64,{encoded}")
        st.subheader("Atmosphere Ramp Texture")

        ramps = clickable_images(
            images,
            titles=ramp_titles,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "20px"},
        )
        st.markdown(f"Status: {ramp_titles[ramps]} selected" if ramps > -1 else "Status: No texture selected")

if st.button("Generate", disabled=True):
    # Add user's maps
    if not os.path.exists(f"_{sys_name}/_PluginData"):
        os.mkdir(f"_{sys_name}/_PluginData")
        os.mkdir(f"_{sys_name}/_PluginData/_Biomes")
    open(name + "_Normal.dds", "wb").write(normal_map.getbuffer())
    open(name + "_Color.dds", "wb").write(color_map.getbuffer())
    open(name + "_Biome.png", "wb").write(biome_map.getbuffer())
    open(name + "_Height.dds", "wb").write(height_map.getbuffer())

    # Generate Localization

    if not os.path.exists(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg"):
        if not os.path.exists(f"_{sys_name}/_Localization"):
            os.mkdir(f"_{sys_name}/_Localization")
        output = open(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg", "w")
        file = '''Localization
    {
        en-us
        {
            #LOC_GU_Planets_''' + name + '''_displayName = ''' + display_name + '''^N
            #LOC_GU_Planets_''' + name + '''_description = ''' + desc + '''<color=#ffb765>Analogous to ''' + display_name + '''.</color>
        }
    }'''
        output.write(file)
        output.close()
    else:
        current_file = open(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg", "r")
        current_file = current_file.read()
        localization_file = open(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg", "w")
        localization_file.write(utils.update_localization(display_name, name, desc, current_file, "Planets"))
        localization_file.close()

    biome_data = ''''''
    id_ = 0
    for biome in st.session_state['biomes']:
        biome_data = biome_data + '''
				{
				Biome
				{
					name = ''' + biome[0] + '''
					displayName = #LOC_GU_Planets_''' + name + '''_BiomeName''' + str(id_) + '''
					value = 1
					color = ''' + str(biome[1]) + '''
				}'''
        id_ += 1
    file = '''@Kopernicus:HAS[@GU_SYSTEM_Settings:HAS[#''' + sys_name + '''[True]]]:FOR[GU]
{
    useOnDemand = true
    Body
    {
		name = ''' + name + '''
		Tag = GU
		cacheFile = GU/_Systems/_''' + sys_name + '''/_Cache/Tur.bin
		Debug
		{
		exportMesh = true
		update = true
		}
		Template
        {
            name = ''' + template + '''
			removeAllPQSMods = True
        }
		Properties
		{
            description = #LOC_GU_Planets_''' + name + '''_description
			displayName = #LOC_GU_Planets_''' + name + '''_displayName
			albedo = ''' + str(alb) + '''
            radius = ''' + str(radius * 636880) + '''
            geeASL = ''' + str(radius * 1.582715739e-06) + '''
			rotationPeriod = ''' + str(rotation) + '''
			rotates = ''' + str(rotates).lower() + '''
			tidallyLocked = ''' + str(not rotates).lower() + '''
			initialRotation = 0
			isHomeWorld = falses
			timewarpAltitudeLimits = 0 ''' + str(0.001256123603 * (radius * 636880)) + ''' ''' + str(
        0.006280618013 * (radius * 636880)) + ''' ''' + str(0.01256123603 * (radius * 636880)) + ''' ''' + str(
        0.03140309006 * (radius * 636880)) + ''' ''' + str(0.06280618013 * (radius * 636880)) + ''' ''' + str(
        0.1256123603 * (radius * 636880)) + ''' ''' + str(0.2512247205 * (radius * 636880)) + '''
			ScienceValues
			{
				landedDataValue = 0 
				flyingLowDataValue = 0 
				flyingHighDataValue = 0
				inSpaceLowDataValue = 0
				inSpaceHighDataValue = 0 
				recoveryValue = 0
				flyingAltitudeThreshold = 0 
				spaceAltitudeThreshold = 0
			}
          
			biomeMap = GU/_Systems/_''' + sys_name + '''/_PluginData/_Biomes/''' + name + '''_Biome.png
			Biomes''' + biome_data + '''
		    }
	    }'''

    id_ = 0
    # Generate curves
    if template == "Laythe" or template == "Jool":
        stefan_boltzmann_constant = 5.670374419 * 10 ** -8
        teff = ((1360 / (sma ** 2)) * (1 - alb) / (4 * stefan_boltzmann_constant)) ** 0.25
        temp_curve = ''''''
        mult_curve = ''''''
        psi_curve = ''''''
        for i in list(st.session_state['temp_curve'].keys()):
            temp_curve = temp_curve + '''            key = ''' + str(i) + ''' ''' + str(list(st.session_state['temp_curve'].values())[id_]) + ''' 0 0
'''
            mult_curve = mult_curve + '''            key = ''' + str(i) + ''' ''' + str(list(st.session_state['temp_curve'].values())[id_] - teff) + ''' 0 0
'''
            psi_curve = psi_curve + '''            key = ''' + str(i) + ''' ''' + str(list(st.session_state['psi_curve'].values())[id_]) + ''' 0 0
'''
            id_ += 1
        # TODO: Assign each ramp with an ambient color
        i = {}
        file = file + '''        Atmosphere				
		{				
		    enabled = True			
		    oxygen = ''' + str(oxygen) + '''	
		    ambientColor = 0,0,0,0	
		    altitude = ''' + str(atm_height) + '''			
		    adiabaticIndex = 1.4			
		    atmosphereMolarMass = ''' + str(molar_mass) + '''
		    temperatureSeaLevel = ''' + str(st.session_state['temp_curve'].get(st.session_state['temp_curve'][0])) + '''			
		    staticPressureASL = ''' + str(st.session_state['psi_curve'].get(st.session_state['psi_curve'][0])) + '''
		temperatureLatitudeBiasCurve
        {
            key = 0 ''' + str(abs(abs(zero_day - zero_night) - teff)) + ''' 0 0
            key = 38 ''' + str(abs(abs(mid_day - mid_night) - teff)) + ''' 0 0
            key = 90 ''' + str(abs(abs(ninety_day - ninety_night) - teff)) + ''' 0 0
        }
        temperatureLatitudeSunMultCurve
        {
            key = 0 ''' + str(
            (abs(mid_night - mid_day) - abs(abs(zero_night - zero_day) - abs(ninety_night - ninety_day))) * numpy.cos(
                0) + abs(abs(zero_night - zero_day) - abs(ninety_night - ninety_day))) + ''' 0 0
            key = 38 ''' + str(
            (abs(mid_night - mid_day) - abs(abs(zero_night - zero_day) - abs(ninety_night - ninety_day))) * numpy.cos(
                38) + abs(abs(zero_night - zero_day) - abs(ninety_night - ninety_day))) + ''' 0 0
            key = 90 ''' + str(
            (abs(mid_night - mid_day) - abs(abs(zero_night - zero_day) - abs(ninety_night - ninety_day))) * numpy.cos(
                90) + abs(abs(zero_night - zero_day) - abs(ninety_night - ninety_day))) + ''' 0 0
        }
        temperatureCurve
        {
''' + temp_curve + '''
        }
        temperatureEccentricityBiasCurve
        {
            key = 0 ''' + str(orb_ecc_var / 2) + ''' 0 -''' + str(orb_ecc_var) + '''
            key = 1 -''' + str(orb_ecc_var / 2) + ''' -''' + str(orb_ecc_var) + ''' 0
        }
        temperatureSunMultCurve
        {
''' + mult_curve + '''
        }
        pressureCurve
        {
''' + psi_curve + '''
        }'''
        file = file + '''
        AtmosphereFromGround
		{
				
			waveLength = 0.65, 0.58, 0.5, 1.0
		}
	}
		ScaledVersion
		{
			type = ''' + ("AtmosphericStandard" if template == "Laythe" else "Vacuum") + '''
			fadeStart = ''' + str(radius * 0.0157015450320312) + '''
			fadeEnd = ''' + str(radius * 0.1020600427082025) + '''
			OnDemand
			{
				texture = GU/_Systems/_''' + sys_name + '''/_PluginData/''' + name + '''_Color.dds
                		normals = GU/_Systems/_''' + sys_name + '''/_PluginData/''' + name + '''_Normal.dds
			}
			Material
			{
				color = 1,1,1,1
				specColor = 0.5,0.5,0.5,1
				shininess = ''' + str(alb * 2) + '''
               	rimPower = 0.75
				rimBlend = 1.25
				rimColorRamp = GU/PluginData/_AtmoRamp/''' + ramp_titles[ramps] + '''_Ramp.dds		
			}
		}'''
        if ocean:
            file = file + '''		Ocean
	{
		ocean = True
		oceanHeight = 0
		density = 1.01
		oceanColor = 0.592307746,0.592307746,0.584615409,1
		Material
		{
			color = 0.592307746,0.592307746,0.584615409,1
			colorFromSpace = 0.178821743,0.280562043,0.319793373,1
			fogColor = 0.321443439,0.611232221,0.747761178,1
			waterTex = GU/Terrain/PluginData/_Ocean/ocean03.dds
			waterTex1 = GU/Terrain/PluginData/_Ocean/ocean04.dds
			bumpMap = GU/Terrain/PluginData/_Ocean/oceannormal.dds
		}
		FallbackMaterial
		{
			color = 0.592307746,0.592307746,0.584615409,1
			colorFromSpace = 0.1095908442,0.14210041,0.196716406,1
			waterTex = GU/Terrain/PluginData/_Ocean/ocean02.dds
			waterTex1 = GU/Terrain/PluginData/_Ocean/ocean01.dds
		}
		Fog
		{
			fogColorEnd = 0.011,0.023,0.035,1
			fogColorStart = 0.116878122,0.236456618,0.356862751,1
			useFog = True
		}
		Mods
		{
			OceanFX
			{
				
				framesPerSecond = 1
				spaceSurfaceBlend = 0.45
				spaceAltitude = ''' + str((radius * 636880) * 0.006280618013) + '''
				enabled = true
				order = 200
				Watermain
				{
					value = GU/Terrain/PluginData/_Ocean/ocean01.dds
					value = GU/Terrain/PluginData/_Ocean/ocean02.dds
					value = GU/Terrain/PluginData/_Ocean/ocean03.dds
					value = GU/Terrain/PluginData/_Ocean/ocean04.dds
					value = GU/Terrain/PluginData/_Ocean/ocean05.dds
					value = GU/Terrain/PluginData/_Ocean/ocean06.dds
					value = GU/Terrain/PluginData/_Ocean/ocean07.dds
					value = GU/Terrain/PluginData/_Ocean/ocean08.dds
					value = GU/Terrain/PluginData/_Ocean/ocean09.dds
					value = GU/Terrain/PluginData/_Ocean/ocean10.dds
					value = GU/Terrain/PluginData/_Ocean/ocean11.dds
					value = GU/Terrain/PluginData/_Ocean/ocean12.dds
					value = GU/Terrain/PluginData/_Ocean/ocean13.dds
					value = GU/Terrain/PluginData/_Ocean/ocean14.dds
					value = GU/Terrain/PluginData/_Ocean/ocean15.dds
					value = GU/Terrain/PluginData/_Ocean/ocean16.dds
					value = GU/Terrain/PluginData/_Ocean/ocean17.dds
					value = GU/Terrain/PluginData/_Ocean/ocean18.dds
					value = GU/Terrain/PluginData/_Ocean/ocean19.dds
					value = GU/Terrain/PluginData/_Ocean/ocean20.dds
					value = GU/Terrain/PluginData/_Ocean/ocean21.dds
				}
			}
		}
	}'''
            # PQS NOTES:
            # Not leaving max and min level to user input, staying as is
            # leave saturation and contrast the same, modify in later versions
            file = file + '''
        PQS
        {
            minLevel = 2
			maxLevel = 8
			minDetailDistance = 8
			maxQuadLengthsPerFrame = 0.03
			fadeStart = ''' + str((radius * 636880) * 0.0157015450320312) + '''
			fadeEnd = ''' + str((radius * 636880) * 0.1020600427082025) + '''
			deactivateAltitude = ''' + str((radius * 636880) * 0.2009797764099987) + '''
			allowFootprints = ''' + str(footprints) + '''
			materialType = AtmosphericTriplanarZoomRotation
			Material
			{
			    factor = 7.5
			    factorBlendWidth = 0.05
				factorRotation = 135
				saturation = 1.05
				contrast = 1.00
				tintColor = 1,1,1,0
				specularColor = 0.0,0.0,0.0,0.1
				albedoBrightness = ''' + str(alb * 6.5) + '''
				steepPower = ''' + str(power) + '''
				steepTexStart = ''' + str((radius * 636880) * 0.007536741615375) + '''
				steepTexEnd = ''' + str((radius * 636880) * 0.1507348323074991) + '''
				steepTex = GU/Terrain/PluginData/''' + titles[steep] + '''.dds
				steepTexScale = 1,1
				steepTexOffset = 0,0
				steepBumpMap = GU/Terrain/PluginData/''' + titles[steep].replace("Color", "Normal") + '''.dds
				steepBumpMapScale = 1,1
				steepBumpMapOffset = 0,0
				steepNearTiling = 250
				steepTiling = 50
				lowTex = GU/Terrain/PluginData/Dusty_Color.dds
				lowTexScale = 1,1
				lowTexOffset = 0,0
				lowTiling = 1
				midTex = GU/Terrain/PluginData/''' + titles[mid] + '''.dds
				midTexScale = 1,1
				midTexOffset = 0,0
				midTiling = 75000
				midBumpMap = GU/Terrain/PluginData/''' + bump_titles[mid_bump] + '''.dds
				midBumpMapScale = 1,1
				midBumpMapOffset = 0,0
				midBumpTiling = 75000
				highTex = GU/Terrain/PluginData/Dusty_Color.dds
				highTexScale = 1,1
				highTexOffset = 0,0
				highTiling = 1
				lowStart = -2
				lowEnd = -2
				highStart = 2
				highEnd = 2
				globalDensity = 1
				planetOpacity = 1
				oceanFogDistance = 1000
			}
			PhysicsMaterial
			{
				bounceCombine = Average
				frictionCombine = Maximum
				bounciness = 0
				staticFriction = 0.8
				dynamicFriction = 0.6
			}
			Mods
			{
			    VertexColorMap
                {
                    map = GU/_Systems/_''' + sys_name + '''/_PluginData/''' + name + '''_Color.dds
                    order = 500
                    enabled = true
                }
                
                VertexHeightMap
                {
                    map = GU/_Systems/_''' + sys_name + '''/_PluginData/''' + name + '''_Height.dds
                    deformity = 7140
                    scaleDeformityByRadius = false
                    order = 20
                    enabled = true
                }
            }
        }
    }
}'''
            if not os.path.exists(f"_{sys_name}/_Celestials"):
                if not os.path.exists(f"_{sys_name}"):
                    os.mkdir(f"_{sys_name}")
                    os.mkdir(f"_{sys_name}/_Celestials")
            output = open(f"_{sys_name}/_Celestials/{name}.cfg", "w")
            output.write(file)
            output.close()

