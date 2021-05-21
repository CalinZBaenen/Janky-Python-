from json import *
from copy import copy
class JankyParser:
    whitespace = [" ","\t","\n"]
    vflg = ["var","let","con"]
    def __init__(this,preserve=False):
        this.preserve = preserve
        this.variables = {}
        c = {
            "Table": {
                "value": [],
                "type": "table",
                "properties": {
                    "length": 0
                }
            },
            "Array": {
                "value": [],
                "type": "array",
                "properties": {
                    "length": 0,
                    "append": {
                        "args": [],
                        "code": []
                    }
                }
            },
            "Object": {
                "value": {},
                "type": "object",
                "properties": {}
            },
            "Function": {
                "value": {"args": [], "code": []},
                "type": "function"
            },
            "Class": {
                "value": {"constructor": {"args": [], "code": []}, "properties": {}},
                "type": "class",
                "properties": {
                    "methods": 1
                }
            },
            "String": {
                "value": "",
                "type": "string",
                "properties": {
                    "length": 0
                }
            },
            "Number": {
                "value": 0,
                "type": "number",
                "properties": {
                    "length": 1
                }
            },
            "pi": {
                "value": 3.14159265359,
                "type": "number",
                "properties": {
                    "length": 12
                }
            },
            "help": {
                "value": "KEYWORDS:\n\tprint (prints any arguements given)\n\tprintforeach (prints a new line for each arguement given)\n\tprintln (prints any arguements given, and adds a new-line)\n\tclear (clears the output console)\nCONSTANTS:\n\tpi\n\thelp\n\tsystemVersion\n\tString\n\tNumber\n\tTable\n\tArray\n\tBoolean\n\tFunction\n\tClass\n\tObject\n\ttrue\n\tfalse\nSYMBOLS:\n\t= (Variable assignment)\n\t. (Property getter)",
                "type": "string",
                "properties": {
                    "keywords": ["print","printforeach","println","clear"],
                    "constants": ["Table","Array","Object","Function","Class","Number","pi","help","systemVersion","Boolean","true","false"],
                    "symbols": ["=","."],
                    "variable_properties": "Properties, all objects or variables come with a default property (usually length) when declared,\nbut if they are objects the only properties they will have is their keys.\nIf you are getting the properties from a non-object variable you have 3 defualt properties to play around with:\n\t.properties\n\t.name\n\t.prototpye",
                    "comments": "As of now (v0.0.1) comments are not currently supported.",
                    "advanced": "For advanced help do:\n\thelp.keywords\n\thelp.constants\n\thelp.comments\n\thelp.variable_properties",
                    "advance": "For advanced help do:\n\thelp.keywords\n\thelp.constants\n\thelp.comments\n\thelp.variable_properties"
                }
            },
            "systemVersion": {
                "value": "0.0.1",
                "type": "systemnumber",
                "properties": {
                    "phase": "beta",
                    "length": 3
                }
            },
            "Boolean": {
                "value": False,
                "type": "boolean",
                "properties": {
                    "on": True,
                    "off": False,
                    "yes": True,
                    "no": False,
                    "y": True,
                    "n": False,
                    "truths": [True,1,"FILLED-STRING",["FILLED-ARRAY"],{"Key": "and value pairs (Objects)"}],
                    "falses": [False,0,"",[],{}]
                }
            },
            "True": {
                "value": True,
                "type": "boolean"
            },
            "False": {
                "value": False,
                "type": "boolean"
            },
            "true": {
                "value": True,
                "type": "boolean"
            },
            "false": {
                "value": False,
                "type": "boolean"
            }
        }
        this.constants = c
        this.dflt = c
        this.constructs = {}
    def parse(this,code):
        # -- Store if an 'if' statement ran its code -- #
        ifexec = []
        # -- Check if preserve mode is active, if not then reset variables etc... -- #
        if not this.preserve:
            this.variables = {}
            this.constants = this.dflt
            this.constructs = {}
        # -- Set up data for packets and information transportation -- #
        packetData = {}
        packets = []
        errors = []
        _placeholder_code_ = ""
        code = code.split(";")
        for s in code:
            _placeholder_code_ += s
        code = _placeholder_code_.split("\n")
        lineNumber = 1
        # -- Shift certain array elements (Used mainly for operations / controls) -- #
        def shiftElementFromTo(array,value,newindex,moveall=False):
            a = []
            indx = 0
            trashdump = []
            for v in array:
                if  v == value:
                    trashdump.append(v)
                    if not moveall:
                        break
            while indx < len(array):
                v = None
                try:
                    v = array[indx]
                except:
                    pass
                if indx == newindex:
                    a += trashdump
                else:
                    if v != value:
                        a.append(array[indx])
                indx += 1
            return a
        # -- Check if a value can be parsed into a number -- #
        def parseable(v):
            litrlStrNm = str(v)
            psbl = False
            try:
                float(litrlStrNm)
            except:
                psbl = False
            else:
                psbl = True
            return psbl
        # -- Parse the value if the before functions returns true -- #
        def parseNumber(v):
            nm = float(str(v))
            if nm - floor(nm) == 0:
                nm = int(nm)
            return nm
        # -- Floor number so non decimals become int datatypes (for illusion sakes) -- #
        def floor(v):
            v2 = round(v)
            if v2 > v:
                v2 -= 1
            return v2
        # -- Change Python 3 native types to Janky types -- #
        def toJT(pyt):
            pyt = str(pyt)
            if "str" in pyt:
                return "string"
            elif "int" in pyt or "float" in pyt:
                return "number"
            elif "bool" in pyt:
                return "boolean"
            elif "list" in pyt:
                return "table"
            elif "dict" in pyt:
                return "object"
            else:
                return "unknown"
        # -- Define what a control should do -- #
        def control(ctrl,val):
            if ctrl == "not":
                return not val
            elif ctrl == "type":
                return toJT(type(val))
        # -- Define what a control for a variable should do -- #
        def varcontrol(ctrl,val,f):
            flg = this.vflg[f]
            hep = {}
            if flg == "var":
                hep = this.variables
            elif flg == "let":
                hep = this.constants
            elif flg == "con":
                hep = this.constructs
            else:
                errors.append(f"Error: Invalid flagging operation in native code")
            if ctrl == "not":
                return not hep[val]["value"]
            elif ctrl == "type":
                return hep[val]["type"]
        # -- Parse each line of code -- #
        for line in code:
            # -- Special 'linenumber' constant -- #
            this.constants["linenumber"] = {
                "value": lineNumber,
                "type": "number"
            }
            line = line + " "
            requestedVarType = "var"
            position = 0
            heap = []
            values = []
            state = 0
            tok = ""
            string = ""
            stringStarter = ""
            get = "value"
            propertyToGet = ""
            command = ""
            controls = []
            ifs = []
            elses = []
            operations = []
            pff = ""
            probj = {}
            for char in line:
                # -- Check for normal strings -- #
                if char == "\"" or char == "'":
                    # -- If a string hasn't stared, stant a new one, else stop the current string -- #
                    if state == 0:
                        state = 1
                        stringStarter = char
                        char = ""
                    elif state == 1 and char == stringStarter:
                        state = 0
                        stringStarter = ""
                        values.append(string)
                        if controls:
                            try:
                                v = control(controls[-1],values[-1])
                                controls.pop()
                                values.pop()
                                values.append(v)
                            except:
                                errors.append(f"Error: Invalid VCO / Comparative symbol at line {lineNumber}")
                        string = ""
                        char = ""
                # -- Check for variable-string strings -- #
                elif char == "`":
                    if state == 0:
                        state = 2
                        stringStarter = char
                        char = ""
                    elif state == 2:
                        state = 0
                        stringStarter = ""
                        for v in this.variables:
                            while "{"+str(v)+"}" in string:
                                string = string.replace("{"+str(v)+"}",str(this.variables[v]["value"]))
                        for v in this.constants:
                            while "{"+str(v)+"}" in string:
                                string = string.replace("{"+str(v)+"}",str(this.constants[v]["value"]))
                        for v in this.constructs:
                            while "{"+str(v)+"}" in string:
                                string = string.replace("{"+str(v)+"}",str(this.constructs[v]["value"]))
                        values.append(string)
                        if controls:
                            try:
                                v = control(controls[-1],values[-1])
                                controls.pop()
                                values.pop()
                                values.append(v)
                            except:
                                errors.append(f"Error: Invalid VCO / Comparative symbol at line {lineNumber}")
                        string = ""
                        char = ""
                # -- Set values to their 'not' version -- #
                elif char == "!" and state == 0:
                    controls.append("not")
                    tok = ""
                    char = ""
                # -- Get properties of an object -- #
                elif char == "." and state == 0 and (tok in this.variables or tok in this.constants or tok in this.constructs):
                    # -- vs: Variabe Self (Get the name of the variable) -- #
                    vs = tok
                    # -- pg: Property Getter -- #
                    pg = None
                    # -- probj: Properties Object -- #
                    probj = None
                    # -- Find where the property is from -- #
                    if tok in this.variables:
                        pg = copy(this.variables[tok])
                    elif tok in this.constants:
                        pg = copy(this.constants[tok])
                    elif tok in this.constructs:
                        pg = copy(this.constructs[tok])
                    # -- Do ckecks on the 'object' it has properties -- #
                    try:
                        # -- If it's an 'object', excuse it's lack of properties -- #
                        if copy(pg["type"]) != "object":
                            probj = copy(copy(pg["properties"]))
                        else:
                            probj = {}
                        # -- Don't add variable specific properties if they are objects -- @
                        if pg["type"] != "object":
                            probj["name"] = vs
                            try:
                                probj["properties"] = json.loads(str(copy(probj)).replace("'","\""))
                            except JSONDecodeError:
                                try:
                                    probj["properties"] = copy(probj)
                                except:
                                    pass
                            except Exception:
                                pass
                            probj["prototype"] = copy(pg)
                        else:
                            try:
                                for key in copy(pg["value"]):
                                    probj[key] = pg["value"][key]
                            except:
                                errors.append(f"Error: Object scanning failed at line {lineNumber}")
                        # -- Say an 'object' has no properties if no key / value pairs are found -- #
                        if copy(pg["type"]) == "object" and probj == {}:
                            raise KeyError
                        pff = "properties"
                    # -- If there are no properties, alert the user -- #
                    except KeyError:
                        errors.append(f"Error: The variable '{tok}' has no properties at line {lineNumber}")
                    # -- Catch other errors -- #
                    except Exception as err:
                        errors.append(f"Error: Native property code failed at line {lineNumber};\n| {err} : {type(err).__name__} : {err.args} |")
                    tok = ""
                    char = ""
                # -- Add to string -- #
                if state == 1 or state == 2:
                    string += char
                # -- Parse keyword/symbol if space is encountered -- #
                if char in this.whitespace and state == 0:
                    char = ""
                    # -- Check if a property can be found -- #
                    # -- Check for properties -- #
                    if pff == "properties" and probj != {} and not tok in this.whitespace:
                        # -- Turn off property finding -- #
                        pff = ""
                        # -- pn: Property Name -- #
                        pn = None
                        pn = tok
                        tok = ""
                        # -- Give the value and clear the properties object -- #
                        try:
                            if pn == "":
                                errors.append(f"Error: Expecting property name after '.' at line {lineNumber}")
                            else:
                                prval = None
                                prval = copy(probj[pn])
                                values.append(copy(prval))
                                prval = None
                                pass
                            pass
                        except:
                            try:
                                errors.append(f"Error: '{probj['name']}' has no property '{pn}' at line {lineNumber}")
                            except Exception as err:
                                errors.append(f"Error: (at line {lineNumber}) Internal property handling error;\n{err}")
                        probj = {}
                        pass
                    # -- Make sure cppo, probj, and pff are clear -- #
                    pff = ""
                    probj = {}
                    # -- See if there is an if statement, and if the value is true, continue running == #
                    if ifs:
                        try:
                            t = values[-1]
                        except:
                            pass
                        else:
                            ifs.pop()
                            t = values[-1]
                            values.pop()
                            ifexec.append(bool(t))
                            if bool(t):
                                pass
                            else:
                                break
                    # -- Run else statements -- #
                    if elses:
                        elses.pop()
                        try:
                            t = ifexec[-1]
                        except:
                            errors.append(f"Error: Invalid 'else' statement at line: {lineNumber}")
                        else:
                            t = ifexec[-1]
                            ifexec.pop()
                            if not t:
                                pass
                            else:
                                break
                    # -- Let numbers exist -- #
                    if parseable(tok):
                        values.append(parseNumber(tok))
                        if controls:
                            try:
                                v = control(controls[-1],values[-1])
                                controls.pop()
                                values.pop()
                                values.append(v)
                            except:
                                errors.append(f"Error: Invalid VCO / Comparative symbol at line {lineNumber}")
                    # -- Make values printable -- #
                    elif tok == "print":
                        command = "print"
                    elif tok == "println":
                        command = "println"
                    # -- Clear the display of text -- #
                    elif tok == "clear":
                        command = "clear"
                    # -- Print a new line for each value -- #
                    elif tok == "printforeach":
                        command = "printforeach"
                    # -- Return type -- #
                    elif tok == "typeof":
                        controls.append("type")
                    # -- Allow creation of all different sorts of variables -- #
                    elif tok == "var":
                        requestedVarType = "var"
                    elif tok == "let":
                        requestedVarType = "let"
                    elif tok == "construct":
                        requestedVarType = "construct"
                    # -- If and Else statements -- #
                    elif tok == "if":
                        ifs.append("if")
                    elif tok == "else":
                        elses.append("else")
                    # -- Assignment for variables -- #
                    elif tok == "=":
                        operations.append("ass")
                    elif tok == "equals":
                        operations.append("s")
                    # -- Retrieve (and / or) reassign variables -- #
                    elif tok in this.variables:
                        if not "ass" in operations:
                            heap.append(tok)
                        values.append(this.variables[tok]["value"])
                        if controls:
                            values.pop()
                            values.append(varcontrol(controls[-1],tok,0))
                    elif tok in this.constants:
                        if not "ass" in operations:
                            heap.append(tok)
                        values.append(this.constants[tok]["value"])
                        if controls:
                            values.pop()
                            values.append(varcontrol(controls[-1],tok,1))
                    elif tok in this.constructs:
                        if not "ass" in operations:
                            heap.append(tok)
                        values.append(this.constructs[tok]["value"])
                        if controls:
                            values.pop()
                            values.append(varcontrol(controls[-1],tok,2))
                    # -- If the token was not able to be applied to any of these, add it to the heap to get assigned -- #
                    else:
                        heap.append(tok)
                    tok = ""
                # -- Add char to tok if it can be -- #
                if state == 0:
                    tok += char
            # -- Remove all blank spaces from heap [fixes bug where last item of heap is: ''] -- #
            while "" in heap:
                heap.remove("")
            # -- Make some simple Order Of Operations (OOO) -- #
            operations = shiftElementFromTo(operations,"ass",len(operations)-1)
            # -- Create an error instance if a string or datatype definition is unclosed, prevents any error in user code, and native python code -- #
            if state:
                errors.append(f"Error: Unexpected EOF / EOL at line: {lineNumber}")
            # -- Execute the OOO -- #
            for o in operations:
                # -- Assign / Reassign variables -- #
                if o == "ass":
                    name = None
                    value = None
                    try:
                        name = heap[-1]
                        value = values[-1]
                    except:
                        name = None
                        value = None
                        errors.append(f"Error: Variable assignment missing name or value at line: {lineNumber}")
                    else:
                        name = heap[-1]
                        value = values[-1]
                        heap.pop()
                        values.pop()
                        if not name in this.constants:
                            inTy = toJT(type(value))
                            if requestedVarType == "var":
                                this.variables[name] = {}
                                this.variables[name]["value"] = value
                                this.variables[name]["type"] = toJT(type(value))
                                if inTy == "string" or inTy == "number":
                                    this.variables[name]["properties"] = {
                                        "length": len(str(value))
                                    }
                            elif requestedVarType == "let":
                                this.constants[name] = {}
                                this.constants[name]["value"] = value
                                this.constants[name]["type"] = toJT(type(value))
                                requestedVarType = "var"
                                if inTy == "string" or inTy == "number":
                                    this.variables[name]["properties"] = {
                                        "length": len(str(value))
                                    }
                            elif requestedVarType == "construct":
                                this.constructs[name] = {}
                                this.constructs[name]["value"] = value
                                this.constructs[name]["type"] = "construct"
                                requestedVarType = "var"
                                if inTy == "string" or inTy == "number":
                                    this.variables[name]["properties"] = {
                                        "length": len(str(value))
                                    }
                            else:
                                errors.append(f"Error: Native code parsing failed at line: {lineNumber}")
                        else:
                            errors.append(f"Error: Can not redefine a constant at line: {lineNumber}")
            # -- Add all sorts of information to packets that WILL be read -- #
            packetData["command"] = command
            packetData["line"] = lineNumber
            packetData["values"] = values
            packetData["heap"] = heap
            packetData["code"] = line
            packetData["errors"] = errors
            packets.append(packetData)
            packetData = {}
            lineNumber += 1
            # -- Stop code execution if there are any errors -- #
            if len(errors) >= 1:
                break
        # -- Give the packets -- #
        return packets