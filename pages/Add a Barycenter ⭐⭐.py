import os
import pathlib

import streamlit as st

import utils

main_pth = str(pathlib.Path(__file__).parent.parent.resolve()).replace('\\', '/')

sys_name = open(f"{main_pth}/sys_name.txt", "r").read()

st.info(
    "Once a Barycenter is created, you can add an object to it via selecting your Barycenter in the Orbiting Info expander.")
name = st.text_input("Name")
dis_name = st.text_input("Display Name")
desc = st.text_area("Description")
rad = st.number_input("Radius (in KAU)")
color = st.color_picker("Color")

with st.expander("Location Info"):
    til = st.number_input("Tilt")
    dis = st.number_input("Distance (in Light Years, from Kerbol)")

if st.button("Generate", disabled=True):
    if not os.path.exists(f"_{sys_name}"):
        os.mkdir(f"_{sys_name}")
    if not os.path.exists(f"_{sys_name}/_Celestials"):
        os.mkdir(f"_{sys_name}/_Celestials")
    if not os.path.exists(f"_{sys_name}/_Celestials/_BaryCenters"):
        os.mkdir(f"_{sys_name}/_Celestials/_BaryCenters")


    if len(str(len(os.listdir(f"_{sys_name}/_Celestials/_BaryCenters")))) == 1:
        center = open(f"_{sys_name}/_Celestials/_BaryCenters/0" + str(
            len(os.listdir(f"_{sys_name}/_Celestials/_BaryCenters")) + 1) + "_" + name + ".cfg",
                      "w")
    else:
        center = open(f"_{sys_name}/_Celestials/_BaryCenters/" + str(
            len(os.listdir(f"_{sys_name}/_Celestials/_BaryCenters")) + 1) + "_" + name + ".cfg",
                      "w")
    file = '''@Kopernicus:HAS[@GU_SYSTEM_Settings:HAS[#Alpha_Centauri[True]]]:FOR[GU]
{
	Body
	{
		name = ''' + name + '''
		Tag = GU
		cacheFile = GU/_Systems/_''' + sys_name + '''/_Cache/''' + name + '''.bin
		Template
		{
			name = Jool
			removeAtmosphere = true
			removeCoronas = true
		}
		Properties
		{
			displayName = #LOC_GU_BaryCenters_''' + name + '''_displayName
			description = #LOC_GU_BaryCenters_''' + name + '''_description
			mass = MASSREPLACE
			radius = ''' + str(rad * 69633999.50956351) + '''
			inverseRotThresholdAltitude = 0
			selectable = True
			hiddenRnD = True
			sphereOfInfluence = SOIREPLACE
		}
		Orbit 
		{
			referenceBody = Sun
        	color = ''' + str(color) + '''
            inclination = ''' + str(til) + '''
        	eccentricity = 0
        	semiMajorAxis = ''' + str(dis * 6.6034488e+14) + '''
        	longitudeOfAscendingNode = 0
        	argumentOfPeriapsis = 0
        	meanAnomalyAtEpoch = 0
        	epoch = 0
        	mode = 0
        	iconTexture = GU/Configs/GU_Icons/starG
		}
		ScaledVersion
		{
			invisible = True
			type = Vacuum
			fadeStart = 0
			fadeEnd = 0
			Material
			{
				color = 0,0,0,0
				specColor = 0,0,0,0
				shininess = 1
			}
		}
		Debug
		{
			exportMesh = true
			update = true
		}
	}
}
	 '''
    center.write(file)
    center.close()

    # Localization
    if not os.path.exists(
            f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg"):
        if not os.path.exists(f"_{sys_name}/_Localization"):
            os.mkdir(f"_{sys_name}/_Localization")
        output = open(
            f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg",
            "w")
        file = '''Localization
{
    en-us
    {
        #LOC_GU_BaryCenters_''' + name + '''_displayName = ''' + dis_name + '''^N
        #LOC_GU_BaryCenters_''' + name + '''_description = ''' + desc + '''<color=#ffb765>Analogous to ''' + dis_name + '''.</color>
    }
}'''
        output.write(file)
        output.close()
    else:
        current_file = open(
            f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg",
            "r")
        current_file = current_file.read()
        localization_file = open(
            f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg",
            "w")
        localization_file.write(utils.update_localization(dis_name, name, desc, current_file, "BaryCenters"))
        localization_file.close()
    st.info(dis_name + " generated successfully!")

with st.expander("Finish Generation (Use after all celestial bodies wanted are orbiting the Barycenter)"):
    name2 = st.text_input(" Name (Ex: AlphaCentauri)")
    if st.button("Finish Generation", disabled=True):
        masses = []
        num_id = 0  # Used for opening the correct file later
        for i in os.listdir("_" + sys_name + "/_Celestials"):
            if "." not in i:
                for i2 in os.listdir("_" + sys_name + "/_Celestials/" + i):
                    if open("_" + sys_name + "/_Celestials/" + i + "/" + i2, "r").readlines()[4].split("= ")[
                        1].replace("\n", "") == name2:
                        num_id = i2.split("_")[0]
                    if "referenceBody = " + name2 in open("_" + sys_name + "/_Celestials/" + i + "/" + i2, "r").read():
                        for line in open("_" + sys_name + "/_Celestials/" + i + "/" + i2, "r").readlines():
                            if "mass" in line:
                                mass = line.split("= ")[1].replace("\n", "")
                                masses.append(float(mass))
            else:
                if "referenceBody = " + name2 in open("_" + sys_name + "/_Celestials/" + i, "r").read():
                    for line in open("_" + sys_name + "/_Celestials/" + i, "r").readlines():
                        if "mass" in line:
                            mass = line.split("= ")[1].replace("\n", "")
                            masses.append(float(mass))
        final_mass = sum(masses)
        soi = final_mass * 2.8407987e-18
        file = open("_" + sys_name + "/_Celestials/_BaryCenters/" + str(num_id) + "_" + name2 + ".cfg",
                    "r").read().replace("MASSREPLACE", str(final_mass)).replace("SOIREPLACE", str(soi))
        wfile = open("_" + sys_name + "/_Celestials/_BaryCenters/" + str(num_id) + "_" + name2 + ".cfg", "w")
        wfile.write(file)
        wfile.close()
        st.info(name2 + " has completed generation!")
