from neqsim import java_gateway
from neqsim import javaGateway

neqsim = java_gateway.jvm.neqsim
ThermodynamicOperations = neqsim.thermodynamicOperations.ThermodynamicOperations
fluidcreator = neqsim.thermo.Fluid
fluid_type = {
    'srk': neqsim.thermo.system.SystemSrkEos,
    'SRK-EoS': neqsim.thermo.system.SystemSrkEos,
    'Psrk-EoS': neqsim.thermo.system.SystemPsrkEos,
    'PSRK-EoS': neqsim.thermo.system.SystemPsrkEos,
    'RK-EoS': neqsim.thermo.system.SystemRKEos,
    'pr': neqsim.thermo.system.SystemPrEos,
    'PR-EoS': neqsim.thermo.system.SystemPrEos,
    'srk-s': neqsim.thermo.system.SystemSrkSchwartzentruberEos,
    'GERG-water': neqsim.thermo.system.SystemGERGwaterEos,
    'SRK-MC': neqsim.thermo.system.SystemSrkMathiasCopeman,
    'PR-MC': neqsim.thermo.system.SystemPrMathiasCopeman,
    'scrk': neqsim.thermo.system.SystemSrkSchwartzentruberEos,
    'ScRK-EoS': neqsim.thermo.system.SystemSrkSchwartzentruberEos,
    'nrtl': neqsim.thermo.system.SystemNRTL,
    'unifac': neqsim.thermo.system.SystemUNIFAC,
    'electrolyte': neqsim.thermo.system.SystemFurstElectrolyteEos,
    'Electrolyte-ScRK-EoS': neqsim.thermo.system.SystemFurstElectrolyteEos,
    'Electrolyte-CPA-EoS': neqsim.thermo.system.SystemElectrolyteCPAstatoil,
    'cpa-el': neqsim.thermo.system.SystemElectrolyteCPA,
    'cpa-s': neqsim.thermo.system.SystemSrkCPAs,
    'cpa-statoil': neqsim.thermo.system.SystemSrkCPAstatoil,
    'CPA-SRK-EoS': neqsim.thermo.system.SystemSrkCPA,
    'cpa-srk': neqsim.thermo.system.SystemSrkCPA,
    'srk-twoCoon': neqsim.thermo.system.SystemSrkTwuCoonParamEos,
    'cpa-pr': neqsim.thermo.system.SystemPrCPA,
    'CPA-PR-EoS': neqsim.thermo.system.SystemPrCPA,
}


def fluid(name='srk', temperature=298.15, pressure=1.01325):
    fluid_function = fluid_type.get(name, neqsim.thermo.system.SystemSrkEos)
    return fluid_function(temperature, pressure)

def createfluid(fluid_type='dry gas'):
    return fluidcreator.create(fluid_type)

def createfluid2(names, molefractions, unit="mol/sec"):
    gateway = javaGateway.JavaGateway()
    double_class = gateway.jvm.double
    string_class = gateway.jvm.String
    numberOfComponents =len(names)    
    compositionJavaArray = gateway.new_array(double_class,numberOfComponents)
    nameJavaArray = gateway.new_array(string_class,numberOfComponents)
    i = 0
    for i in range(0,numberOfComponents):
        compositionJavaArray[i] = molefractions[i]
        nameJavaArray[i] = names[i]
        i = i+1
    return fluidcreator.create2(nameJavaArray, compositionJavaArray, unit)

def addOilFractions(fluid, charNames,molefractions,molarMass,  density):
    gateway = javaGateway.JavaGateway()
    double_class = gateway.jvm.double
    string_class = gateway.jvm.String
    numberOfComponents =len(charNames)    
    compositionJavaArray = gateway.new_array(double_class,numberOfComponents)
    molarMassJavaArray = gateway.new_array(double_class,numberOfComponents)
    relDensityJavaArray = gateway.new_array(double_class,numberOfComponents)
    nameJavaArray = gateway.new_array(string_class,numberOfComponents)
    i = 0
    for i in range(0,numberOfComponents):
        compositionJavaArray[i] = molefractions[i]
        nameJavaArray[i] = charNames[i]
        molarMassJavaArray[i] = molarMass[i]
        relDensityJavaArray[i] = density[i]
        i = i+1
    clonedfluid = fluid.clone()
    clonedfluid = fluidcreator.addOilFractions(nameJavaArray, compositionJavaArray, molarMassJavaArray, relDensityJavaArray)
    return clonedfluid;

def newdatabase(system):
    system.createDatabase(1)
    
def data(system):
    a = system.getResultTable()
    return a

def table(system):
    return system.createTable("")

def dataFrame(system):
    import pandas
    system.createTable("")
    return pandas.DataFrame(system.createTable(""))
    
def printFrame(system):
    import pandas
    system.createTable("")
    print(pandas.DataFrame(system.createTable("")).to_string(header=False, index=False))

def printFluid(system):
    a = system.getResultTable()
    for i in range(len(a)):
        for j in range(len(a[i])):
            print(a[i][j], end='\t')
    print()

def volumecorrection(system, use=1):
    system.useVolumeCorrection(use)


def write(system, filename, newfile=0):
    system.write(filename, filename, newfile)


def appenddatabase(system):
    system.createDatabase(0)


def show(system):
    system.display()


def showPDF(system):
    system.generatePDF()
    system.displayPDF()


def addComponent(thermoSystem, name, moles, unit="no", phase=-10):
    if phase == -10 and unit == "no":
        thermoSystem.addComponent(name, moles)
    elif phase == -10:
        thermoSystem.addComponent(name, moles, unit)
    elif unit == "no":
        thermoSystem.addComponent(name, moles, phase)
    else:
        thermoSystem.addComponent(name, moles, unit, phase)


def temperature(thermoSystem, temp, phase=-1):
    if phase == -1:
        thermoSystem.setTemperature(temp)
    else:
        thermoSystem.getPhase(phase).setTemperature(temp)


def pressure(thermoSystem, pres, phase=-1):
    if phase == -1:
        thermoSystem.setPressure(pres)
    else:
        thermoSystem.getPhase(phase).setPressure(pres)


def reactionCheck(thermoSystem):
    thermoSystem.chemicalReactionInit()


def mixingRule(thermoSystem, mixRule='classic', GEmodel=''):
    if GEmodel == '':
        thermoSystem.setMixingRule(mixRule)
    else:
        thermoSystem.setMixingRule(mixRule, GEmodel)


def multiphase(testSystem, multiphase=1):
    testSystem.setMultiPhaseCheck(multiphase)


def solidcheck(testSystem, solid=1):
    testSystem.setSolidPhaseCheck(solid)


def solid(testSystem, solid=1):
    testSystem.setSolidPhaseCheck(solid)


def TPflash(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TPflash()
    testSystem.init(3)
    
def PVTpropTable(fluid1, fileName, lowTemperature, highTemperature, Tsteps, lowPressure, highPressure, Psteps):
    testFlash = ThermodynamicOperations(fluid1)
    testFlash.OLGApropTable(lowTemperature, highTemperature, Tsteps, lowPressure, highPressure, Psteps, fileName, 0);
    testFlash.displayResult();

def TPsolidflash(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.TPSolidflash()

def PHflash(testSystem, enthalpy):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.PHflash(enthalpy, 0)
    
def PHsolidflash(testSystem, enthalpy):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.PHsolidFlash(enthalpy)


def PSflash(testSystem, entropy):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.PSflash(entropy)


def freeze(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.freezingPointTemperatureFlash()
    
def scaleCheck(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.checkScalePotential(testSystem.getPhaseNumberOfPhase("aqueous"))
    testFlash.display()

def ionComposition(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.calcIonComposition(testSystem.getPhaseNumberOfPhase("aqueous"))
    testFlash.display()


def hydp(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.hydrateFormationPressure()

def addfluids(fluid1, fluid2):
    return neqsim.thermo.system.SystemInterface.addFluids(fluid1,fluid2)

def hydt(testSystem, type=1):
    if not testSystem.doHydrateCheck():
        testSystem.setHydrateCheck(True)
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.hydrateFormationTemperature(type)
    return testSystem.getTemperature()

def calcIonComposition(fluid1):
    testFlash = ThermodynamicOperations(fluid1)
    testFlash.calcIonComposition(fluid1.getPhaseNumberOfPhase("aqueous"))
    return testFlash.getResultTable()
    
def checkScalePotential(fluid1):
    testFlash = ThermodynamicOperations(fluid1)
    testFlash.checkScalePotential(fluid1.getPhaseNumberOfPhase("aqueous"))
    return testFlash.getResultTable()

def bubp(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.bubblePointPressureFlash(0)
    except:
        print('error calculating bublepoint')
    return testSystem.getPressure()

def bubt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.bubblePointTemperatureFlash()
    except:
        print('error calculating bublepoint')
    return testSystem.getTemperature()


def dewp(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.dewPointPressureFlash()
    except:
        print('error could not calculate')
    return testSystem.getPressure()


def dewt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.dewPointTemperatureFlash()
    except:
        print('error could not calculate')
    return testSystem.getTemperature()


def waterdewt(testSystem):
    testFlash = ThermodynamicOperations(testSystem)
    try:
        testFlash.waterDewPointTemperatureFlash()
    except:
        print('error could not calculate')
    return testSystem.getTemperature()


def phaseenvelope(testSystem, plot=False):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.calcPTphaseEnvelope()
    data = testFlash
    if(plot):
        import matplotlib.pyplot as plt
        plt.plot(list(data.getOperation().get("dewT") ),list(data.getOperation().get("dewP")), label="dew point")
        plt.plot(list(data.getOperation().get("bubT")),list(data.getOperation().get("bubP")), label="bubble point")

        try:
            plt.plot(list(data.getOperation().get("dewT2")),list(data.getOperation().get("dewP2")), label="dew point2")
        except:
            pass
            #print("An exception occurred")

        try:
            plt.plot(list(data.getOperation().get("bubT2")),list(data.getOperation().get("bubP2")), label="bubble point2")
        except:
            pass
            #print("An exception occurred")
        
        plt.title('PT envelope')
        plt.xlabel('Temperature [K]')
        plt.ylabel('Pressure [bar]')
        plt.legend()
        plt.show()
    return testFlash

def fluidComposition(testSystem, composition):
    gateway = javaGateway.JavaGateway()
    double_class = gateway.jvm.double
    numberOfComponents =len(composition)    
    compositionJavaArray = gateway.new_array(double_class,numberOfComponents)
    i = 0
    for i in range(0,numberOfComponents):
        compositionJavaArray[i] = composition[i]
        i = i+1
    testSystem.setMolarComposition(compositionJavaArray)
    testSystem.init(0)

def getExtThermProp(function, thermoSystem, t=0, p=0):
    nargout = [0, 0, 0, 0]
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
        TPflash(thermoSystem)
    thermoSystem.init(3)
    nargout[0] = function[0]() / thermoSystem.getNumberOfMoles()
    if (thermoSystem.getNumberOfPhases() == 1):
        if (thermoSystem.getPhase(0).getPhaseType == 1):
            nargout[1] = function[1]() / thermoSystem.getPhase(0).getNumberOfMolesInPhase()
            nargout[2] = 0
        else:
            nargout[2] = function[1]() / thermoSystem.getPhase(0).getNumberOfMolesInPhase()
            nargout[1] = 0
    else:
        nargout[1] = function[1]() / thermoSystem.getPhase(0).getNumberOfMolesInPhase()
        nargout[2] = function[2]() / thermoSystem.getPhase(1).getNumberOfMolesInPhase()

    nargout[3] = thermoSystem.getNumberOfPhases()
    return nargout


def getIntThermProp(function, thermoSystem, t=0, p=0):
    nargout = [0, 0, 0, 0]
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
        TPflash(thermoSystem)
    thermoSystem.init(3)
    nargout[0] = function[0]()
    if (thermoSystem.getNumberOfPhases() == 1):
        if (thermoSystem.getPhase(0).getPhaseType == 1):
            nargout[1] = function[1]()
            nargout[2] = 0
        else:
            nargout[2] = function[1]()
            nargout[1] = 0
    else:
        nargout[1] = function[1]()
        nargout[2] = function[2]()

    nargout[3] = thermoSystem.getNumberOfPhases()
    return nargout


def getPhysProp(function, thermoSystem, t=0, p=0):
    nargout = [0, 0, 0, 0]
    if t != 0:
        thermoSystem.setTemperature(t)
        if p != 0:
            thermoSystem.setPressure(p)
        TPflash(thermoSystem)
    thermoSystem.init(3)
    thermoSystem.initPhysicalProperties()
    nargout[0] = function[0]()
    if (thermoSystem.getNumberOfPhases() == 1):
        if (thermoSystem.getPhase(0).getPhaseType == 1):
            nargout[1] = function[1]()
            nargout[2] = 0
        else:
            nargout[2] = function[1]()
            nargout[1] = 0
    else:
        nargout[1] = function[1]()
        nargout[2] = function[2]()

    nargout[3] = thermoSystem.getNumberOfPhases()
    return nargout


def enthalpy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getEnthalpy)
    func.append(thermoSystem.getPhase(0).getEnthalpy)
    func.append(thermoSystem.getPhase(1).getEnthalpy)
    return getExtThermProp(func, thermoSystem, t, p)


def entropy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getEntropy)
    func.append(thermoSystem.getPhase(0).getEntropy)
    func.append(thermoSystem.getPhase(1).getEntropy)
    return getExtThermProp(func, thermoSystem, t, p)

def densityGERG2008(phase):
    GERG2008 = neqsim.thermo.util.GERG.NeqSimGERG2008();
    return GERG2008.getDensity(phase)

def molvol(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getMolarVolume)
    func.append(thermoSystem.getPhase(0).getMolarVolume)
    func.append(thermoSystem.getPhase(1).getMolarVolume)
    return getIntThermProp(func, thermoSystem, t, p)


def energy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getInternalEnergy)
    func.append(thermoSystem.getPhase(0).getInternalEnergy)
    func.append(thermoSystem.getPhase(1).getInternalEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def gibbsenergy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getGibbsEnergy)
    func.append(thermoSystem.getPhase(0).getGibbsEnergy)
    func.append(thermoSystem.getPhase(1).getGibbsEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def helmholtzenergy(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getHelmholtzEnergy)
    func.append(thermoSystem.getPhase(0).getHelmholtzEnergy)
    func.append(thermoSystem.getPhase(1).getHelmholtzEnergy)
    return getExtThermProp(func, thermoSystem, t, p)


def molefrac(thermoSystem, comp, t=0, p=0):
    func = []
    func.append(thermoSystem.getPhase(0).getComponent(comp).getz)
    func.append(thermoSystem.getPhase(0).getComponent(comp).getx)
    func.append(thermoSystem.getPhase(1).getComponent(comp).getx)
    return getIntThermProp(func, thermoSystem, t, p)


def moles(thermoSystem, phase=0):
    if phase == 0:
        return thermoSystem.getNumberOfMoles()
    else:
        return thermoSystem.getPhase(phase).getNumberOfMolesInPhase()


def beta(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getBeta)
    func.append(thermoSystem.getPhase(0).getBeta)
    func.append(thermoSystem.getPhase(1).getBeta)
    return getIntThermProp(func, thermoSystem, t, p)


def molarmass(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getMolarMass)
    func.append(thermoSystem.getPhase(0).getMolarMass)
    func.append(thermoSystem.getPhase(1).getMolarMass)
    return getIntThermProp(func, thermoSystem, t, p)


def Z(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getZ)
    func.append(thermoSystem.getPhase(0).getZ)
    func.append(thermoSystem.getPhase(1).getZ)
    return getIntThermProp(func, thermoSystem, t, p)


def density(thermoSystem, volcor=1, t=0, p=0):
    func = []
    func.append(thermoSystem.getDensity)
    if volcor == 1:
        thermoSystem.initPhysicalProperties()
        func.append(thermoSystem.getPhase(0).getPhysicalProperties().getDensity)
        func.append(thermoSystem.getPhase(1).getPhysicalProperties().getDensity)
    else:
        func.append(thermoSystem.getPhase(0).getDensity)
        func.append(thermoSystem.getPhase(1).getDensity)
    return getPhysProp(func, thermoSystem, t, p)


def viscosity(thermoSystem, t=0, p=0):
    func = []
    func.append(thermoSystem.getPhase(0).getPhysicalProperties().getViscosity)
    func.append(thermoSystem.getPhase(0).getPhysicalProperties().getViscosity)
    func.append(thermoSystem.getPhase(1).getPhysicalProperties().getViscosity)
    return getPhysProp(func, thermoSystem, t, p)

def PVTpropTable(testSystem,fileName, lowTemperature, highTemperature, Tsteps, lowPressure, highPressure, Psteps):
    testFlash = ThermodynamicOperations(testSystem)
    testFlash.OLGApropTable(lowTemperature, highTemperature, Tsteps, lowPressure, highPressure, Psteps, fileName, 0) 
