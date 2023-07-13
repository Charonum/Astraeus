import os

import streamlit as st
import pathlib
import utils


main_pth = str(pathlib.Path(__file__).parent.parent.resolve()).replace('\\', '/')

sys_name = open(f"{main_pth}/sys_name.txt", "r").read()

name = st.text_input("Name")
display_name = st.text_input("Display Name")
desc = st.text_area("Description")
cont_weight = st.slider("Contract Weight", max_value=50)
radius = st.number_input("Radius (1 = Radius of Kerbol)")
mass = st.number_input("Mass (1 = Mass of Kerbol)")
lum = st.number_input("Luminosity (1 = Luminosity of Kerbol)")
rotates = st.checkbox("Black Hole Rotates", value=True)
rotation = st.number_input("Rotation Period (sec)")
color = st.color_picker("Color")

st.warning(
    "Only ONE Expander may be used. Fill out Location Info if this black hole isn't orbiting anything, or use Orbiting Info to define this black hole's orbit around an object.")
with st.expander("Location Info"):
    til = st.number_input("Tilt")
    dis = st.number_input("Distance (in Light Years, from Kerbol)")

with st.expander(
        "Orbiting Info"):
    options = ["Nothing"]
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
        os.mkdir(f"_{sys_name}")
        os.mkdir(f"_{sys_name}/_Celestials")
        for i in os.listdir("_" + sys_name + "/_Celestials"):
            if "." not in i:
                for i2 in os.listdir("_" + sys_name + "/_Celestials/" + i):
                    try:
                        options.append(i2.replace(".cfg", "").split("_")[1])
                    except:
                        options.append(i2.replace(".cfg", ""))
            else:
                options.append(i.replace(".cfg", ""))
    orb = st.selectbox("Orbiting:", options=options)
    per = st.number_input("Period (in days)")
    inc = st.number_input("Inclination/ Tilt (in degrees)")
    ecc = st.number_input("Eccentricity")
    sma = st.number_input("Semi Major Axis (in KAU)")
    loam = st.number_input("Longitude of Ascending Node (in degrees)")
    aop = st.number_input("Argument of Periapsis (in degrees)")
    ma = st.number_input("Mean Anomaly at Epoch")

if st.button("Generate", disabled=True):

    file = '''@Kopernicus:HAS[@GU_SYSTEM_Settings:HAS[#The_Singularity[True]]]:FOR[GU]
{
	Body
	{
	name = ''' + name + f'''
	Tag = GU
	cacheFile = GU/_Systems/_''' + sys_name + '''/_Cache/''' + name + '''.bin
	contractWeight = 0
	Template
		{
			name = Sun
			removeCoronas = true
		}
	Debug
		{
			exportMesh = true
			update = false
		}
        
        Properties
        {
	    displayName = #LOC_GU_Stars_''' + name + '''_displayName
            description = #LOC_GU_Stars_''' + name + '''_description
            radius = ''' + str(radius * 69633999.50956351) + '''
    	    mass = ''' + str(mass * 1.9950101e+28) + '''
	    rotationPeriod = ''' + str(rotation) + '''
	    rotates = ''' + str(rotates).lower() + '''
	    sphereOfInfluence = ''' + str((radius * 1.9950101e+28) * 2.8407987e-18) + '''    
	}'''
    if orb != "Nothing":
        for i in os.listdir("_" + sys_name + "/_Celestials"):
            if "." not in i:
                for i2 in os.listdir("_" + sys_name + "/_Celestials/" + i):
                    try:
                        if i2.split("_")[1] == orb + ".cfg":
                            orb = i2.split("_")[1].replace(".cfg", "")
                            break
                    except:
                        pass
            else:
                if orb + ".cfg" == i:
                    orb = i.replace(".cfg", "")
                    break
        file = file + '''
                Orbit
                {
                	referenceBody = ''' + str(orb) + '''
                	color = 1,1,2,1
                	inclination = ''' + str(inc) + '''
                	eccentricity = ''' + str(ecc) + '''
                	semiMajorAxis = ''' + str(sma) + '''
                	longitudeOfAscendingNode = ''' + str(loam) + '''
                	argumentOfPeriapsis = ''' + str(aop) + '''
                	meanAnomalyAtEpoch = ''' + str(ma) + '''
                	mode = 0
                	iconTexture = GU/Configs/GU_Icons/blackhole
                }'''
    else:
        file = file + '''
        		Orbit
        		{
        			referenceBody = Sun
        			color = 1,1,2,1
                	inclination = ''' + str(til) + '''
        			eccentricity = 0
        			semiMajorAxis = ''' + str(dis * 6.6034488e+14) + '''
        			longitudeOfAscendingNode = 0
        			argumentOfPeriapsis = 0
        			meanAnomalyAtEpoch = 0
        			epoch = 0
        			mode = 0
        			iconTexture = GU/Configs/GU_Icons/blackhole
        		}'''
    file = file + '''
        Atmosphere
		{
			enabled = True
			oxygen = False
			adiabaticIndex = 1.23
			altitude = ''' + str((radius * 69633999.50956351) * 3.410503634) + '''
			
			gasMassLapseRate = 0
			atmosphereMolarMass = 0
			pressureCurveIsNormalized = False
	
			temperatureCurveIsNormalized = False
			temperatureLapseRate = 0
			temperatureSeaLevel = 10000000 
		
			pressureCurve
			{
				key = 0 	0 		0 		0
				key = ''' + str((radius * 69633999.50956351) * 3.410503634) + ''' 	0 		0 		0
			}
			temperatureCurve
			{
				key = 0 	10000000 	0 		0
				key = ''' + str((radius * 69633999.50956351) * 3.410503634) + '''	1000 	0 		0
			}
			AtmosphereFromGround
			{
				
				waveLength = 0,0,0,0 
			}
		}
	ScaledVersion
        {
            Light
			{
				sunFlare = GU/Configs/RerumNovarumNoGhosts.unity3d:sun_flare
				sunlightColor = ''' + color + '''
				IntensityCurve
				{
					key = 0 1.25 0 0
					key = 1.4959787e+12 0.55 0 0		
					key = 7.4798935E+14 0 0 0
				}
				sunlightShadowStrength = 1
				scaledSunlightColor = ''' + color + '''
				ScaledIntensityCurve
				{
					key = 0 1.25 0 0
					key = 249329784.5 0.55 0 0
					key = 124664891667 0 0 0
				}
				IVASunColor = ''' + color + '''
				IVAIntensityCurve
				{
					key = 0 1.25 0 0
					key = 249329784.5 0.55 0 0
					key = 124664891667 0 0 0
				}
				sunLensFlareColor = ''' + color + '''
				sunAU = 500000000000
				luminosity = ''' + str(lum) + '''
				brightnessCurve
				{
					key = 0 0.0075 0 0
					key = 0.001 0.025 0 0
					key = 0.01 0.25 0 0
					key = 0.1 1 0 0
					key = 1 2 0 0
					key = 10 5 0 0
					key = 11 0 0 0
					key = 20 0 0 0

				}
			}
	     Material
            	{
                
		rimColor = 1,1,1,1
		rimPower = -2.5
		rimBlend = 0.001
		emitColor0 = 0,0,0,1
		emitColor1 = 0,0,0,1
		sunspotColor = 0,0,0,0
		sunspotPower = 0
            }	
        }
    }
}'''

    print("Generating Config...")
    if not os.path.exists(f"_{sys_name}/_Celestials/_StellarObjects"):
        if not os.path.exists(f"_{sys_name}"):
            os.mkdir(f"_{sys_name}")
            os.mkdir(f"_{sys_name}/_Celestials")
            os.mkdir(f"_{sys_name}/_Celestials/_StellarObjects")
        elif not os.path.exists(f"_{sys_name}/_Celestials"):
            os.mkdir(f"_{sys_name}/_Celestials")
        elif not os.path.exists(f"_{sys_name}/_Celestials/_StellarObjects"):
            os.mkdir(f"_{sys_name}/_Celestials/_StellarObjects")
    output = open(f"_{sys_name}/_Celestials/_StellarObjects/{name}.cfg", "w")
    output.write(file)
    output.close()
    print("Config Generated!")

    print("Generating Language File...")

    if not os.path.exists(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg"):
        if not os.path.exists(f"_{sys_name}/_Localization"):
            os.mkdir(f"_{sys_name}/_Localization")
        output = open(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg", "w")
        file = '''Localization
{
    en-us
    {
        #LOC_GU_Stars_''' + name + '''_displayName = ''' + display_name + '''^N
        #LOC_GU_Stars_''' + name + '''_description = ''' + desc + '''<color=#ffb765>Analogous to ''' + display_name + '''.</color>
    }
}'''
        output.write(file)
        output.close()
    else:
        current_file = open(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg", "r")
        current_file = current_file.read()
        localization_file = open(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg", "w")
        localization_file.write(utils.update_localization(display_name, name, desc, current_file, "Stars"))
        localization_file.close()
    print("Generated Language File!")

    print("Generating Singularity Config")

    if not os.path.exists(f"_{sys_name}/_Configs/GU_Patches/_Singularity"):
        os.mkdir(f"_{sys_name}/_Configs")
        os.mkdir(f"_{sys_name}/_Configs/GU_Patches")
        os.mkdir(f"_{sys_name}/_Configs/GU_Patches/_Singularity")
    file = '''Singularity
	{
		Singularity_object
			{
				name = ''' + name + '''
				gravity = ''' + str((mass * 1.9950101e+28) * 2.4531669e-26) + '''
				hideCelestialBody = True
				useAccretionDisk = True
				useRadialTextureMapping = False
				accretionDiskNormal = 0,1,0
				accretionDiskInnerRadius = 0
				accretionDiskOuterRadius = ''' + str(mass * 1.9950101e+28 * 3) + '''
				accretionDiskRotationSpeed = -0.5
				accretionDiskTexturePath = GU/PluginData/_Core/ACCRBH.png
				scaleEnclosingMesh = 1
				depthWrite = False
			}
		}
	}
}'''
    singularity = open(f"_{sys_name}/_Configs/GU_Patches/_Singularity/Singularity{name}.cfg",
                       "w")
    singularity.write(file)
    singularity.close()

    st.info(f"{str(name)} generated successfully!")
