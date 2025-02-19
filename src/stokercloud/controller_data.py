import decimal
from enum import Enum


class NotConnectedException(Exception):
    pass

class PowerState(Enum):
    on  = 1
    off = 0

class Unit(Enum):
    KWH = 'kwh'
    PERCENT = 'pct'
    DEGREE = 'deg'
    KILO_GRAM = 'kg'
    GRAM = 'g'
    M3H = 'm3/h'
    CELSIUS = 'C'
    PASCAL = 'pa'

class State(Enum):
    ROZPALANIE_1 = 'lng_state_2'
    ROZPALANIE_2 = 'lng_state_4'
    MOC = 'lng_state_5'
    CWU = 'lng_state_7'
    ZATRZYM_TempOsiag = 'lng_state_9'
    BLAD_ROZPAL = 'lng_state_13'
    WYLACZONY = 'lng_state_14'
    ZATRZYM_BrakPelletu = 'lng_state_20'
    CZUW_Harmon = 'lng_state_23'
    CZUW_TempOsiag = 'lng_state_25'

STATE_BY_VALUE = {key.value: key for key in State}

class Value:
    def __init__(self, value, unit):
        self.value = decimal.Decimal(value)
        self.unit = unit

    def __eq__(self, other):
        if not isinstance(other, Value):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.value == other.value and self.unit == other.unit

    def __repr__(self):
        return "%s %s" % (self.value, self.unit)

def get_from_list_by_key(lst, key, value):
    for itm in lst:
        if itm.get(key) == value:
            return itm

class ControllerData:
    def __init__(self, data):
        if data['notconnected'] != 0:
            raise NotConnectedException("Boiler not connected to StokerCloud")
        self.data = data

    def get_sub_item(self, submenu, _id):
        return get_from_list_by_key(self.data[submenu], 'id', _id)

    @property
    def alarm(self):
        return {
            0: PowerState.off,
            1: PowerState.on
        }.get(self.data['miscdata'].get('alarm'))

    @property
    def running(self):
        return {
            0: PowerState.off,
            1: PowerState.on
        }.get(self.data['miscdata'].get('running'))

    @property
    def serial_number(self):
        return self.data['serial']

    @property
    def boiler_temperature_current(self):
        return Value(self.get_sub_item('frontdata', 'boilertemp')['value'], Unit.DEGREE)

    @property
    def boiler_temperature_requested(self):
        return Value(self.get_sub_item('frontdata', '-wantedboilertemp')['value'], Unit.DEGREE)

    @property                                                                                                      
    def hotwater_temperature_current(self):                                                                        
        return Value(format(self.get_sub_item('frontdata', 'dhw')['value'], '.1f'), Unit.DEGREE)                                  
                                                                                                                   
    @property                                                                                                      
    def hotwater_temperature_requested(self):                                                                      
        return Value(self.get_sub_item('frontdata', 'dhwwanted')['value'], Unit.DEGREE)                            

    @property                                                                                                      
    def oxygen_reference(self):                                                                                    
        return Value(self.get_sub_item('frontdata', 'refoxygen')['value'], Unit.PERCENT)                           
                                                                                                                   
    @property                                                                                                      
    def smoke_temperature(self):                                                                                    
        return Value(format(self.get_sub_item('frontdata', 'smoketemp')['value'], '.1f'), Unit.DEGREE)                           
                                                                                                                   
    @property                                                                                                      
    def airflow(self):                                                                                             
        return Value(self.get_sub_item('frontdata', 'refair')['value'], Unit.M3H) #Airflow m3/h                    

    @property                                                                                                      
    def hopper_distance(self):                                                                                    
        return Value(self.get_sub_item('frontdata', 'hopperdistance')['value'], Unit.PERCENT)                           
                                                                                                                   
    @property                                                                                                      
    def pressure(self):                                                                                    
        return Value(self.get_sub_item('frontdata', 'pressure')['value'], Unit.PASCAL)                           

    @property                                                                                                      
    def exhaust(self):                                                                                            
        return Value(self.get_sub_item('frontdata', 'exhaust')['value'], Unit.PERCENT)                             

    @property                                                                                                      
    def ashdist(self):                                                                                            
        return Value(self.get_sub_item('frontdata', 'ashdist')['value'], Unit.PERCENT)                             
                                                                                                                   
    @property
    def boiler_kwh(self):
        return Value(self.get_sub_item('boilerdata', '5')['value'], Unit.KWH)

    @property                                                                                                      
    def boiler_percent(self):                                                                                          
        return Value(self.get_sub_item('boilerdata', '4')['value'], Unit.PERCENT)                                      

    @property                                                                                                      
    def oxygen_current(self):                                                                                      
        return Value(self.get_sub_item('boilerdata', '12')['value'], Unit.PERCENT) #O2                             
                                                                                                                   
    @property                                                                                                      
    def oxygen_low(self):                                                                                          
        return Value(self.get_sub_item('boilerdata', '14')['value'], Unit.PERCENT) #O2 low                         
                                                                                                                   
    @property                                                                                                      
    def oxygen_mid(self):                                                                                          
        return Value(self.get_sub_item('boilerdata', '15')['value'], Unit.PERCENT) #O2 mid                         
                                                                                                                   
    @property                                                                                                      
    def oxygen_high(self):                                                                                         
        return Value(self.get_sub_item('boilerdata', '16')['value'], Unit.PERCENT) #O2 high                        
                                                                                                                   
    @property                                                                                                      
    def boiler_temp_return(self):                                                                                          
        return Value(self.get_sub_item('boilerdata', '17')['value'], Unit.DEGREE)                                      

    @property                                                                                                      
    def boiler_temp_dropshaft(self):                                                                                          
        return Value(format(self.get_sub_item('boilerdata', '7')['value'], '.1f'), Unit.DEGREE)                                      

    @property                                                                            
    def state(self):                                                                           
        return STATE_BY_VALUE.get(self.data['miscdata']['state']['value']).name      

    @property                                                                            
    def clock(self):                                                                           
        return self.data['miscdata']['clock']['value']      

    @property                                                                                         
    def state_pom(self):                                                                                  
        return self.data['miscdata']['state']['value']                       

    @property
    def consumption_total(self):
        return Value(self.get_sub_item('hopperdata', '4')['value'], Unit.KILO_GRAM)
    
    @property
    def consumption_day(self):
        return Value(self.get_sub_item('hopperdata', '3')['value'], Unit.KILO_GRAM)

    @property                                                                                  
    def auger_capacity(self):                                                                        
        return Value(self.get_sub_item('hopperdata', '2')['value'], Unit.GRAM) #Auger capacity                                         

    @property                                                                                                      
    def hopper_content(self):                                                                                      
        return Value(self.get_sub_item('hopperdata', '1')['value'], Unit.KILO_GRAM)                    
                                                                                                                   
    @property                                                                                                      
    def hopper_trip1(self):                                                                                        
        return Value(self.get_sub_item('hopperdata', '5')['value'], Unit.KILO_GRAM)                                            
                                                                                                                   
    @property                                                                                                      
    def hopper_trip2(self):                                                                                        
        return Value(self.get_sub_item('hopperdata', '13')['value'], Unit.KILO_GRAM)                                             
                                                                                                                   
    @property                                                                                  
    def power_10_percent(self):                                                                        
        return Value(self.get_sub_item('hopperdata', '7')['value'], Unit.KWH) #Power 10%                                          
                                                                                               
    @property                                                                                  
    def power_100_percent(self):                                                                        
        return Value(self.get_sub_item('hopperdata', '8')['value'], Unit.KWH) #Power 100%                                          
                                                                                               
    @property                                                                                   
    def dhw_pump(self):                                                                              
        return self.data['leftoutput']['output-1']['val'].lower()                                                                                                

    @property                                                                                   
    def boiler_pump(self):                                                                              
        return self.data['leftoutput']['output-2']['val'].lower()         
                                                                                                
    @property                                                                                   
    def weather_zone1_valve_position(self):                                                                              
        return self.data['leftoutput']['output-3']['val']         
                                                                                                
    @property                                                                                   
    def weather_pump(self):                                                                              
        return self.data['leftoutput']['output-4']['val'].lower()         

    @property                                                                                   
    def exhaust_fan(self):                                                                              
        return self.data['leftoutput']['output-5']['val'] #Exhaust fan        
                                                                                                
    @property                                                                                   
    def l_6(self):                                                                              
        return self.data['leftoutput']['output-6']['val']         
                                                                                                
    @property                                                                                   
    def compressor_cleaning(self):                                                                              
        return Value(self.data['leftoutput']['output-7']['val'], Unit.KILO_GRAM) #Compressor cleaning       
                                                                                                
    @property                                                                                   
    def l_8(self):                                                                              
        return self.data['leftoutput']['output-8']['val']        
                                                                                               
    @property                                                                                   
    def weather_pump2(self):                                                                              
        return self.data['leftoutput']['output-9']['val'].lower()         
                                                                                                
    @property                                                                                  
    def dhw_difference_under(self):                                                                        
        return Value(self.get_sub_item('dhwdata', '3')['value'], Unit.DEGREE) #DHW-Difference under                                          

    @property                                                                                  
    def hopper_distance_max(self):                                                                          
        return self.data['miscdata'].get('hopper.distance_max')                                       
                                                                                               
    @property                                                                                  
    def weather_zone1_active(self):                                                                             
        return self.data['weathercomp'].get('zone1active')                                      
                                                                                               
    @property                                                                                  
    def weather_zone2_active(self):                                                                             
        return self.data['weathercomp'].get('zone2active')                                      
                                                                                               
    @property                                                                                  
    def zone1_flow_wanted(self):                                                                             
        return Value(format(float(self.data['weathercomp']['zone1-wanted']['val']), '.1f'), Unit.DEGREE)                                
                                                                                               
    @property                                                                                  
    def zone1_flow_current(self):                                                                             
        return Value(format(float(self.data['weathercomp']['zone1-actual']['val']), '.1f'), Unit.DEGREE)                                
                                                                                               
    @property                                                                                  
    def zone1_valve_position(self):                                                                             
        return self.data['weathercomp']['zone1-valve']['val']                               
                                                                                               
    @property                                                                                  
    def zone1_current_temperature(self):                                                                             
        return Value(format(float(self.data['weathercomp']['zone1-actualref']['val']), '.1f'), Unit.DEGREE)                               
                                                                                               
    @property                                                                                  
    def zone1_avarage_temperature(self):                                                                             
        return Value(format(float(self.data['weathercomp']['zone1-calc']['val']), '.1f'), Unit.DEGREE)                               
                                                                                               
    @property                                                                                  
    def zone2_flow_wanted(self):                                                                            
        return Value(format(float(self.data['weathercomp']['zone2-wanted']['val']), '.1f'), Unit.DEGREE)
                                                                                               
    @property                                                                                  
    def zone2_flow_current(self):                                                                            
        return Value(format(float(self.data['weathercomp']['zone2-actual']['val']), '.1f'), Unit.DEGREE)                               
                                                                                               
    @property                                                                                  
    def zone2_valve_position(self):                                                                            
        return self.data['weathercomp']['zone2-valve']['val']                                
                                                                                               
    @property                                                                                  
    def zone2_current_temperature(self):                                                                            
        return Value(format(float(self.data['weathercomp']['zone2-actualref']['val']), '.1f'), Unit.DEGREE)                            
                                                                                         
    @property                                                                                  
    def zone2_avarage_temperature(self):                                                                            
        return Value(format(float(self.data['weathercomp']['zone2-calc']['val']), '.1f'), Unit.DEGREE) 
