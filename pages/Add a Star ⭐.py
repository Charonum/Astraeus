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
rotation = st.number_input("Rotation Period (sec)")
lum = st.number_input("Luminosity (1 = Luminosity of Kerbol)")
temp = st.number_input("Surface Temperature (K)")
color = st.color_picker("Color")

st.warning(
    "Only ONE Expander may be used. Fill out Location Info if this star isn't orbiting anything, or use Orbiting Info to define this star's orbit around an object.")
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
    ecc = st.number_input("Eccentricity ")
    sma = st.number_input("Semi Major Axis (in KAU)")
    loam = st.number_input("Longitude of Ascending Node (in degrees)")
    aop = st.number_input("Argument of Periapsis (in degrees)")
    ma = st.number_input("Mean Anomaly at Epoch")


if st.button("Generate", disabled=True):

    file = '''@Kopernicus:HAS[@GU_SYSTEM_Settings:HAS[#''' + sys_name + '''[True]]]:FOR[GU]
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
	    rotationPeriod = ''' + str(rotation) + '''
	    //starLuminosity = ''' + str(lum) + '''
	    geeASL = ''' + str(radius * 2.37092902e-7) + '''
	    sphereOfInfluence = ''' + str((mass * 1.9950101e+28) * 2.8407987e-18) + '''
	    hillsphere = ''' + str((mass * 1.9950101e+28) * 2.8407987e-18) + '''
	    //G2-yellow dwarf
           
        }'''
    if orb != "Nothing":
        try:
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
        except:
            pass
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
                	iconTexture = GU/Configs/GU_Icons/starG
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
        			iconTexture = GU/Configs/GU_Icons/starG
        		}'''
    # No pressure curves for stars. Might add later
    # Lazy temperature curves
    file = file + '''
		Atmosphere
		{
			enabled = True
			oxygen = False
			maxAltitude = ''' + str(radius * 69633999.50956351 * 0.007277829437) + '''
			adiabaticIndex = 1.23
			atmosphereMolarMass = 0.0022
			staticPressureASL = 0.123365408
			pressureCurve
			{
				key = 0 	0.123365408 	0 -0.000198502
			}
			temperatureSeaLevel = 5790
			temperatureCurve
			{
				key = 0 ''' + str(temp) + ''' 0 0	//Surface				
				key = ''' + str(radius * 69633999.50956351 * 1.1) + ''' ''' + str(temp * 449.0500863557858) + ''' 0 0		
				key = ''' + str(radius * 69633999.50956351 * 1.173843457527732) + ''' ''' + str(temp * 0.0644001727115717) + ''' 0 0
				key = ''' + str(radius * 69633999.50956351 * 26294.0934486) + ''' ''' + str(temp * 8.635578583765112e-4) + ''' 0 0	
				key = ''' + str(radius * 69633999.50956351 * 234768.691506) + ''' 2.52 0 0
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
				key = 0 2 0 0					//Surface
             	key = 149597870.7 2 0 0			//0.01 AU
                key = 747989353.5 1.64 0 0		//0.05 AU
                key = 1495978707 1.48	0 0		//0.1 AU
                key = 7479893535 1.16 0 0		//0.5 AU
                key = 14959787070 1.05 0 0		//1 AU 
				key = 29919574140 0.94 0 0		//2 AU
				key = 74798935350 0.82 0 0		//5 AU
				key = 149597870700 0.74 0 0		//10 AU
				key = 299195741400 0.66 0 0		//20 AU
                key = 747989353500 0.58 0 0		//50 AU
				key = 7.4798935E+12 0.41 0 0	//500 AU
				key = 4.7154039E+13 0 0 0		// edge SOI	
				}
				sunlightShadowStrength = 0.7523364
				ScaledIntensityCurve
				{
				key = 0 2 0 0				
                key = 24932.97845 2 0 0		
                key = 124664.89225 1.64 0 0	
				key = 249329.7845 1.48 0 0	
               	key = 1246648.9225 1.16 0 0	
                key = 2493297.845 1.05 0 0			
				key = 4986595.69 0.94 0 0		
				key = 12466489.225 0.82 0 0		
				key = 24932978.45 0.74 0 0		
				key = 49865956.9 0.66 0 0		
                key = 124664892.25 0.58 0 0		
				key = 1246648916.67 0.41 0		
				key = 7859006500 0 0 0			
				}
				scaledSunlightColor = ''' + str(color) + '''
				
				IVASunColor = ''' + str(color) + '''
				IVAIntensityCurve
				{
				key = 0 2 0 0				
                key = 24932.97845 2 0 0		
                key = 124664.89225 1.64 0 0	
				key = 249329.7845 1.48 0 0	
               	key = 1246648.9225 1.16 0 0	
                key = 2493297.845 1.05 0 0			
				key = 4986595.69 0.94 0 0		
				key = 12466489.225 0.82 0 0		
				key = 24932978.45 0.74 0 0		
				key = 49865956.9 0.66 0 0		
                key = 124664892.25 0.58 0 0		
				key = 1246648916.67 0.41 0		
				key = 7859006500 0 0 0					
				}
				ambientLightColor = 0.05,0.05,0.05,0.05
				sunLensFlareColor = ''' + str(color) + '''
				givesOffLight = True
				sunAU = 60000000000
				luminosity = 2065.84
				radiationFactor = 1.83678
				insolation = 0.2277
				brightnessCurve
				{
					key = 0 0.01 0 0
					key = 0.001 0.025 0 0
					key = 0.01 0.25 0 0
					key = 0.1 1 0.2527741 0.2527741
					key = 11.87831 3.41908 0.1803607 0.1803607
					key = 50 10 0.139929 0.139929
					key = 200 30 0 0

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
					rotation = 180
					Material
					{
						texture = GU/PluginData/_Core/Rays6000.dds
						mainTexScale = 0.99000001,0.850000024
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
					rotation = 100
					Material
					{
						texture = GU/PluginData/_Core/Glow6000.dds
						mainTexScale = 0.949999988,0.949999988
						mainTexOffset = 0,0
						invFade = 2.553731
					}
				}
			}
			Material
			{
				rampMap = GU/PluginData/_Core/Sunspot_clear.png
				rampMapScale = 1,1
				rampMapOffset = 0,0
				noiseMap = GU/PluginData/_Core/Sunspot_clear.png
				noiseMapScale = 1,1
				noiseMapOffset = 0,0
				emitColor0 = 0,0,0,0
				emitColor1 = 0,0,0,0
				sunspotTex = GU/PluginData/_Core/Sunspot_clear.png
				sunspotTexScale = 1,1
				sunspotTexOffset = 0,0
				sunspotPower = 4
				sunspotColor = 0.72307688,0.692308307,0.650000215,1
				rimColor = 0.592307746,0.561538458,0.538461208,1
				rimPower = -0.1
				rimBlend = 0.8
			}
        	}
    	}
}'''

    print("Generating Config...")
    if not os.path.exists(f"_{open('sys_name.txt', 'r').read()}/_Celestials/_StellarObjects"):
        if not os.path.exists(f"_{open('sys_name.txt', 'r').read()}"):
            os.mkdir(f"_{open('sys_name.txt', 'r').read()}")
            os.mkdir(f"_{open('sys_name.txt', 'r').read()}/_Celestials")
            os.mkdir(f"_{open('sys_name.txt', 'r').read()}/_Celestials/_StellarObjects")
        elif not os.path.exists(f"_{open('sys_name.txt', 'r').read()}//_Celestials"):
            os.mkdir(f"_{open('sys_name.txt', 'r').read()}/_Celestials")
        elif not os.path.exists(f"_{open('sys_name.txt', 'r').read()}/_Celestials/_StellarObjects"):
            os.mkdir(f"_{open('sys_name.txt', 'r').read()}/_Celestials/_StellarObjects")
    output = open(f"_{open('sys_name.txt', 'r').read()}/_Celestials/_StellarObjects/{name}.cfg", "w")
    output.write(file)
    output.close()
    print("Config Generated!")
    print("Generating Language File...")

    if not os.path.exists(f"_{open('sys_name.txt', 'r').read()}/_Localization/System_{sys_name}_en-us.cfg"):
        if not os.path.exists(f"_{open('sys_name.txt', 'r').read()}/_Localization"):
            os.mkdir(f"_{open('sys_name.txt', 'r').read()}/_Localization")
        output = open(f"_{open('sys_name.txt', 'r').read()}/_Localization/System_{sys_name}_en-us.cfg", "w")
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
        current_file = open(f"_{open('sys_name.txt', 'r').read()}/_Localization/System_{sys_name}_en-us.cfg", "r")
        current_file = current_file.read()
        localization_file = open(f"_{open('sys_name.txt', 'r').read()}/_Localization/System_{sys_name}_en-us.cfg", "w")
        localization_file.write(utils.update_localization(display_name, name, desc, current_file, "Stars"))
        localization_file.close()
    print("Generated Language File!")
    st.info(f"{str(name)} generated successfully!")