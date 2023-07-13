import glob
import os

import streamlit as st
import pathlib
import shutil

import utils


# TODO: Fix luminosity bug
sys_name = open(f"sys_name.txt", "r").read()

name = st.text_input("Name")
display_name = st.text_input("Display Name")
desc = st.text_area("Description")
cont_weight = st.slider("Contract Weight", max_value=50)
radius = st.number_input("Radius (1 = Radius of Kerbol)")
mass = st.number_input("Mass (1 = Mass of Kerbol)")
lum = st.number_input("Luminosity (1 = Luminosity of Kerbol)")
color = st.color_picker("Color")

st.warning(
    "Only ONE Expander may be used. Fill out Location Info if this pulsar isn't orbiting anything, or use Orbiting Info to define this pulsar's orbit around an object.")
with st.expander("Location Info"):
    til = st.number_input("Tilt (in degrees)")
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
        pass
    orb = st.selectbox("Orbiting:", options=options)
    per = st.number_input("Period (in days)")
    inc = st.number_input("Inclination/ Tilt (in degrees)")
    ecc = st.number_input("Eccentricity")
    sma = st.number_input("Semi Major Axis (in KAU)")
    loam = st.number_input("Longitude of Ascending Node (in degrees)")
    aop = st.number_input("Argument of Periapsis (in degrees)")
    ma = st.number_input("Mean Anomaly at Epoch")

if st.button("Generate", disabled=True):

    # Generating the F I L E
    file = '''@Kopernicus:FOR[GU]
{
    Body
    {
        name = ''' + name + '''
	Tag = GU
		cacheFile = GU/_Systems/_''' + sys_name + '''/_Cache/''' + name + '''.bin
		contractWeight = 0
		Debug
		{
			exportMesh = True 
			update = False
		}
        Template
        {
            name = Sun
        }
        Properties
        {
	    displayName = #LOC_GU_Stars_''' + name + '''_displayName
        description = #LOC_GU_Stars_''' + name + '''_description
        radius = ''' + str(radius * 69633999.50956351) + '''
	    //mass = ''' + str(mass * 1.9950101e+28) + '''
	    rotationPeriod = 1
	    geeASL = 9999
	    sphereOfInfluence = ''' + str((mass * 1.9950101e+28) * 2.8407987e-18) + '''
	    hillsphere = ''' + str((mass * 1.9950101e+28) * 2.8407987e-18) + '''
	    //pulsar

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
                	color = ''' + str(color) + '''
                	inclination = ''' + str(inc) + '''
                	eccentricity = ''' + str(ecc) + '''
                	semiMajorAxis = ''' + str(sma) + '''
                	longitudeOfAscendingNode = ''' + str(loam) + '''
                	argumentOfPeriapsis = ''' + str(aop) + '''
                	meanAnomalyAtEpoch = ''' + str(ma) + '''
                	iconTexture = GU/Configs/GU_Icons/neutron
                }'''
    else:
        file = file + '''
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
        			iconTexture = GU/Configs/GU_Icons/neutron
        		}'''
    file = file + '''
Atmosphere
		{
			enabled = True
			oxygen = False
			maxAltitude = 594.388
			adiabaticIndex = 1.23
			atmosphereMolarMass = 0.0022
			staticPressureASL = 0.123365408
			pressureCurve
			{
				key = 0 	0.123365408 	0 -0.000198502
				key = 10.000 	0.0113365408 	-0.000224043 -0.000224043
				key = 50.000 	0.000856649396 	-0.000125455 -0.000125455
				key = 110.000 	0.000856649396 	-4.05306E-05 -4.05306E-05
				key = 150.000 	0.000856649396 	-1.09283E-05 -1.09283E-05
				key = 190.000 	0.000856649396 	-3.88715E-06 -3.88715E-06
				key = 230.000 	0.000856649396 	-1.42358E-06 -1.42358E-06
				key = 250.000 	0.0000000649396 -5.27357E-07 -5.27357E-07
				key = 270.000 	0.000000009396 	-1.73637E-07 -1.73637E-07
				key = 620.000 	0 0 0
			}
			temperatureSeaLevel = 28856
			temperatureCurve
			{
				key = 0 28856 0 0		//Surface				
				key = 594.388 25000 0 0		//Atmosphere *~1km			
				key = 7479.893535 372.877 0 0	//start HZ
				key = 62000000 150000000
				key = 64000000 250000000	
				key = 65000000 100
				key = 506000000 5 0 0
				key = 520000000 5 0 0
				key = 598391484 2.52 0 0
			}
			AtmosphereFromGround
			{
				
				waveLength = 0,0,0.0
			}
		}
		
		ScaledVersion
        	{
            	Light
			{
				sunFlare = GU/Configs/GUFlare.unity3d:sun_flare_white_core
				sunlightColor = ''' + str(color) + '''
				IntensityCurve
				{
					
					key = 0 3 0 0				
					key = 1495978707 1.5 0 0		// 0.1 AU
                    			key = 14959787070 1 0 0			// 1 AU
					key = 149597870700 0.14 0 0		// 10 AU
                    			key = 4.716981E+13 0 0 0		
				}
				sunlightShadowStrength = 0.7523364
				scaledSunlightColor = ''' + str(color) + '''
				ScaledIntensityCurve
				{
					key = 0 3 0 0				
					key = 24932.97845 1.5 0 0		// 0.1 AU
                    			key = 249329.7845 1 0 0			// 1 AU
					key = 2493297.845 0.14 0 0		// 10 AU
                    			key = 7861635000 0 0 0					
				}
				IVASunColor = ''' + str(color) + '''
				IVAIntensityCurve
				{
					key = 0 3 0 0				
					key = 24932.97845 1.5 0 0		// 0.1 AU
                    			key = 249329.7845 1 0 0			// 1 AU
					key = 2493297.845 0.14 0 0		// 10 AU
                    			key = 7861635000 0 0 0				
				}
				ambientLightColor = 0.05,0.05,0.05,0.05
				sunLensFlareColor = 1,1.25,2,1
				givesOffLight = True
				sunAU = 75998064
				luminosity = ''' + str(l) + '''
				radiationFactor = 1.69355835E-7
				insolation = 2.0994525E-8
				brightnessCurve
				{
					key = 0 0.0052 0 0
					key = 0.001 0.25 0 0
					key = 0.01 0.75 0 0
					key = 0.1 1 0 0
					key = 10 10 0 0
					key = 50 25 0 0
					key = 100 75 0 0
					key = 200 175 0 0
					key = 500 200 0 0
				}
			}
			Coronas
			{
				Value
				{
					scaleSpeed = 0.007
					scaleLimitY = 10
					scaleLimitX = 5
					updateInterval = 5
					speed = -1
					rotation = 75
					Material
					{
						texture = GU/PluginData/_Core/Glow25000.dds
						mainTexScale = 0.949999988,0.949999988
						mainTexOffset = 0,0
						invFade = 2.553731
					}
				}
				Value
				{
					scaleSpeed = 0.007
					scaleLimitY = 10
					scaleLimitX = 5
					updateInterval = 5
					speed = -1
					rotation = 75
					Material
					{
						texture = GU/PluginData/_Core/Glow15000.dds
						mainTexScale = 0.980000019,0.75
						mainTexOffset = 0,0
						invFade = 2.553731
					}
				}
			}
			Material
			{
				rampMap = BUILTIN/
				rampMapScale = 1,1
				rampMapOffset = 0,0
				noiseMap = GU/PluginData/_Core/Sunspot_clear.png
				noiseMapScale = 1,1
				noiseMapOffset = 0,0
				emitColor0 = 1,1,1,1
				emitColor1 = 2,2,2,1
				sunspotTex = GU/PluginData/_Core/Sunspot_clear.png
				sunspotTexScale = 1,1
				sunspotTexOffset = 1500,-1000
				sunspotPower = 0.85
				sunspotColor = 0.0500000007,0.0423076339,1,1
				rimColor = 1,1,1.10000002,1
				rimPower = 0.15
				rimBlend = 0.75
			}
        	}
    	}
}
'''

    print("Generating Config...")

    # -------------------------Main File Generation-------------------------
    if not os.path.exists(f"_{sys_name}/_Celestials/_StellarObjects"):
        if not os.path.exists(f"_{sys_name}"):
            os.mkdir(f"_{sys_name}")
            os.mkdir(f"_{sys_name}/_Celestials")
            os.mkdir(f"_{sys_name}/_Celestials/_StellarObjects")
        elif not os.path.exists(f"_{sys_name}//_Celestials"):
            os.mkdir(f"_{sys_name}/_Celestials")
        elif not os.path.exists(f"_{sys_name}/_Celestials/_StellarObjects"):
            os.mkdir(f"_{sys_name}/_Celestials/_StellarObjects")
    output = open(f"_{sys_name}/_Celestials/_StellarObjects/{name}.cfg", "w")
    output.write(file)
    output.close()
    print("Config Generated!")

    print("Generating Language File...")

    # -------------------------Localization Generation-------------------------

    # Path Generation
    if not os.path.exists(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg"):
        if not os.path.exists(f"_{sys_name}/_Localization"):
            os.mkdir(f"_{sys_name}/_Localization")

        # File Creation
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

        # Add new data to localization file
        current_file = open(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg", "r")
        current_file = current_file.read()
        localization_file = open(f"_{sys_name}/_Localization/System_{sys_name}_en-us.cfg", "w")
        localization_file.write(utils.update_localization(display_name, name, desc, current_file, "Stars"))
        localization_file.close()
    print("Generated Language File!")

    # -------------------------Insanitator Generation-------------------------

    # Path Generation
    if not os.path.exists(f"_{sys_name}/_Configs"):
        os.mkdir(f"_{sys_name}/_Configs")
    if not os.path.exists(f"_{sys_name}/_Configs"):
        os.mkdir(f"_{sys_name}/_Configs")
    if not os.path.exists(f"_{sys_name}/_Configs/GU_Patches"):
        os.mkdir(f"_{sys_name}/_Configs/GU_Patches")
    if not os.path.exists(f"_{sys_name}/_Configs/GU_Patches/_Insanitator"):
        os.mkdir(f"_{sys_name}/_Configs/GU_Patches/_Insanitator")

    # Pasting Pulsar Data

    origin = str(pathlib.Path(__file__).parent.parent.resolve()) + "\\pulsar_resources\\"
    target = f"_{sys_name}/_Configs/GU_Patches/_Insanitator/"

    files = os.listdir(origin)
    png_pattern = os.path.join(target, '*.png')

    png_files = glob.glob(png_pattern)

    if png_files:
        pass
    else:
        for file_name in files:
            shutil.copy(origin + file_name, target + file_name)

    # The F  I  L  E (Yes it's sloppy)

    file = '''INSTANTIATOR
{
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Halo
		Body = ''' + name + '''
		Scale = 70, 70, 0.001 
		Shader = Unlit/Transparent
		Rotation = 0, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_Halo
		Type = Billboard  
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet1
		Body = ''' + name + '''
		Scale = 20500, 0.001, 20500
		Shader = Unlit/Transparent
		Rotation = 60, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_1.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Cocoon1
		Body = ''' + name + '''
		Scale = 20500, 0.001, 20500
		Shader = Unlit/Transparent
		Rotation = 60, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_2
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet2
		Body = ''' + name + '''
		Scale = 175000, 0.001, 175000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 90
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_1.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Cocoon2
		Body = ''' + name + '''
		Scale = 175000, 0.001, 175000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 90
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_2
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet3
		Body = ''' + name + '''
		Scale = 1750000, 0.001, 1750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_1.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Cocoon3
		Body = ''' + name + '''
		Scale = 1750000, 0.001, 1750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_2
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Cocoon4
		Body = ''' + name + '''
		Scale = 8750000, 0.001, 8750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 90
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_2
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet4
		Body = ''' + name + '''
		Scale = 8750000, 0.001, 8750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 90
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_1.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Cocoon5
		Body = ''' + name + '''
		Scale = 43750000, 0.001, 43750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_2
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet5
		Body = ''' + name + '''
		Scale = 43750000, 0.001, 43750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_1.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Cocoon6
		Body = ''' + name + '''
		Scale = 218750000, 0.001, 218750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 90
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_2
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet6
		Body = ''' + name + '''
		Scale = 218750000, 0.001, 218750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 90
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_1.2
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet7
		Body = ''' + name + '''
		Scale = 1093750000, 0.001, 1093750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_3.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet8
		Body = ''' + name + '''
		Scale = 5468750000, 0.001, 5468750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 90
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_3.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet9
		Body = ''' + name + '''
		Scale = 27343750000, 0.001, 27343750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_3.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT
	{
		Name = ''' + name + ''' Jet10
		Body = ''' + name + '''
		Scale = 30343750000, 0.001, 30343750000
		Shader = Unlit/Transparent
		Rotation = 60, 0, 90
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/Pulsar_3.1
		Type = Cube 
		IgnoreLight = true
	}
	SCALED_OBJECT:NEEDS[!Singularity]
	{
		Name = ''' + name + ''' Disk
		Body = ''' + name + '''
		Scale = 500000, 0.001, 500000
		Shader = Unlit/Transparent
		Rotation = 0, 0, 0
		InvertNormals = false
		Texture = GU/_Systems/_''' + sys_name + '''/_Configs/GU_Patches/_Instantiator/bluedisk4
		Type = Cube 
		IgnoreLight = true
	}
}'''

    # File Generation

    config = open(f"_{sys_name}/_Configs/GU_Patches/_Insanitator/{name}.cfg", "w")
    config.write(file)
    config.close()

    # -------------------------Singularity Generation-------------------------

    # Path Generation
    #  No need for _Config and GU_Patches generation, as Insanitator generation takes care of that
    if not os.path.exists(f"_{sys_name}/_Configs/GU_Patches/_Singularity"):
        os.mkdir(f"_{sys_name}/_Configs/GU_Patches/_Singularity")

    # The shorter F I L E
    file = '''Singularity
	{
		Singularity_object
			{
				name = ''' + name + '''
				gravity = ''' + str(mass * 1.257248e-32) + '''
				hideCelestialBody = False
				useAccretionDisk = True
				useRadialTextureMapping = False
				accretionDiskNormal = 0,1,0
				accretionDiskInnerRadius = 2500
				accretionDiskOuterRadius = 22000
				accretionDiskRotationSpeed = -100
				wormholeTarget = 
				accretionDiskTexturePath = GU/PluginData/_Core/ACCR1.png
				scaleEnclosingMesh = 150
				depthWrite = False
			}
		}
    	}
}'''

    # File Generation

    singularity = open(f"_{sys_name}/_Configs/GU_Patches/_Singularity/Singularity{name}.cfg",
                       'w')
    singularity.write(file)
    singularity.close()
    st.info(f"{str(name)} generated successfully!")
