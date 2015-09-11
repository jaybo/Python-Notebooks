import math

# Measured values
MeasuredLuminanceLux = 1.36 
MeasuredLensDiameterInches = 3
MeasuredLensLoss = 0.9

class Sensor():
    def __init__(self, name, pixels, areaInSqMeters, fillFactor, quantumEfficiency, wellDepthInElectrons):
        self.name = name
        self.pixels = pixels
        self.areaInSqMeters = areaInSqMeters
        self.fillFactor = fillFactor
        self.quantumEfficiency = quantumEfficiency
        self.wellDepthInElectrons = wellDepthInElectrons
        self.areaPerPixelInSqMeters = self.areaInSqMeters / self.pixels

sensors = [
    #                                 pixels     areaInSqMeters  FF    QE    Well
    Sensor('FTF2021M',              2032 * 2044, .0243 * .0245, 0.94, 0.50, 250000),
    Sensor('CMOSIS 20000',          5120 * 3840, .0328 * .0246, 0.94, 0.45,  15000),
    Sensor('Canon EOS 7D Mark II',  5472 * 3648, .022  * .015 , 0.94, 0.59,  29544), 
    Sensor('Canon EOS 5DS',         8688 * 5792, .0359 * .024 , 0.94, 0.50,  32498), 
    Sensor('Canon T6s (760D)',      6000 * 4000, .0223 * .0149, 0.94, 0.50,  22065), 
    Sensor('Nikon 7200',            6000 * 4000, .0235 * .0156, 0.94, 0.53,  36048), 
    Sensor('Nikon D810',            7380 * 4928, .0359 * .024 , 0.94, 0.47,  78083), 
    Sensor('Nikon D5500',           6000 * 4000, .0235 * .0156, 0.94, 0.58,  34466), 
    # USB2 Sensor('Sony a7R',              7392 * 4920, .0359 * .0240, 0.94, 0.50,  85000),
    # USB2 Sensor('Canon EOS 7D',          5360 * 3515, .0223 * .0149, 0.94, 0.41,  20129), 
    ]

# 1 lumen = 4.12e+15 photons / m^2  / sec at 555nM

PhotonsPerSquareMeterPerSec = 4.12e+15 * MeasuredLuminanceLux
LensRadiusInMeters = (MeasuredLensDiameterInches / 2) * 0.0254 # inches to meters
AreaOfLensSurfaceInSqMeters = math.pi * LensRadiusInMeters * LensRadiusInMeters 
PhotonsReachingLensSurfacePerSec = PhotonsPerSquareMeterPerSec * AreaOfLensSurfaceInSqMeters

for sensor in sensors:
    sensor.photonsReachingSensor = PhotonsReachingLensSurfacePerSec * MeasuredLensLoss
    sensor.electronsOnSensorPerSec = sensor.photonsReachingSensor * sensor.fillFactor * sensor.quantumEfficiency 
    sensor.electronsOnSensorPerPixelPerSec = sensor.electronsOnSensorPerSec / sensor.pixels
    sensor.exposureTimeToFillWell =  sensor.wellDepthInElectrons / sensor.electronsOnSensorPerPixelPerSec
   
    print '{0:20} fillTime: {1:-4.0f}mS  {2:-4.1f}Mpix  pixArea: {3:-5.1f}uM^2'.format(sensor.name, 
                                                                    1000 * sensor.exposureTimeToFillWell,
                                                                    sensor.pixels / 1e+6, 
                                                                    1e+12 * sensor.areaPerPixelInSqMeters) 



