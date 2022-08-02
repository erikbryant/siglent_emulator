"""Emulate commands common to all Siglent function generators.

Command set is based on the SDG Series Programming Guide:
https://siglentna.com//wp-content/uploads/dlm_uploads/2019/12/SDG_Programming-Guide_PG02-E04A.pdf

TODO:
* Honor the CHDR setting when returning responses.
* Make sure derived classes override their appropriate methods.
* Support parsing of incoming long commands as well as short commands.
"""

from abc import ABC, abstractmethod
import logging
import re
from typing import Dict, List

from siglent_emulator.function_generator import util

# pylint: disable=line-too-long, broad-except

Commands: List[str] = [
    "*OPC?",
    # Unknown why it hangs
    # "CHDR?",
    "C1:MDWV?",
    "C2:MDWV?",
    "C1:SWWV?",
    "C2:SWWV?",
    "C1:BTWV?",
    "C2:BTWV?",
    "C1:ARWV?",
    "C2:ARWV?",
    "C1:SYNC?",
    "C2:SYNC?",
    "NBFM?",
    "LAGG?",
    "SCFG?",
    "BUZZ?",
    "SCSV?",
    "ROSC?",
    "FCNT?",
    "C1:INVT?",
    "C2:INVT?",
    "COUP?",
    "VOLTPRT?",
    "STL?",
    # Unknown why it hangs
    # "C1:WVDT? 0",
    # "C2:WVDT? 0",
    # "C1:WVDT? 59",
    # "C2:WVDT? 59",
    # Has no query form
    # "VKEY",
    "SYST:COMM:LAN:IPAD?",
    "SYST:COMM:LAN:SMAS?",
    "SYST:COMM:LAN:GAT?",
    "C1:SRATE?",
    "C2:SRATE?",
    "C1:HARM?",
    "C2:HARM?",
    "C1:CMBN?",
    "C2:CMBN?",
    "MODE?",
    # Unknown why it hangs
    # "CASCADE?",
    # Not supported on 1032X
    # ":IQ:CENT",
    # ":IQ:SAMP",
    # ":IQ:SYMB",
    # ":IQ:AMPL",
    # ":IQ:IQAD:GAIN",
    # ":IQ:IQAD:IOFF",
    # ":IQ:IQAD:QOFF",
    # ":IQ:IQAD:QSK",
    # ":IQ:TRIG:SOUR",
    # ":IQ:WAVE:BUIL",
    # ":IQ:WAVE:USER",
    # ":IQ:FrequencySampling",
]

channel_defaults: Dict[str, str] = {
    "OUTPUT": "OFF",
    "WVTP": "SINE",
    "FRQ": "1000",
    "PERI": "0.001",
    "AMP": "4",
    "AMPVRMS": "1.414",
    "AMPDBM": "19.99738",
    "OFST": "0",
    "HLEV": "2",
    "LLEV": "-2",
    "PHSE": "0",
    "LOAD": "HZ",
    "PLRT": "NOR",
    "MAX_OUTPUT_AMP": "20",
}


class SDGChannel(ABC):
    """Emulate an SDG series function generator output channel."""

    cvals = channel_defaults.copy()
    channel: int

    def __init__(self, channel: int) -> None:
        self.channel = channel

    @abstractmethod
    def outp(self, command: str) -> str:
        """Proccess all variants of the OUTP command."""
        cvals = self.cvals
        if command == "OUTP?":
            return f"C{self.channel}:OUTP {cvals['OUTPUT']},LOAD,{cvals['LOAD']},PLRT,{cvals['PLRT']}"

        if not command.startswith("OUTP "):
            errlog.error("Unknown command format: '%s'", command)
            return ""

        # Iterate through each command (e.g., 'C1:OUTP ON,LOAD,50,PLRT,NOR')
        sub_cmds = command.split(" ")
        sub_cmds = sub_cmds[1].split(",")
        i: int = 0
        while i < len(sub_cmds):
            cmd = sub_cmds[i]

            if cmd in ["ON", "OFF"]:
                cvals["OUTPUT"] = cmd
                i += 1
                continue

            if cmd == "LOAD":
                param = sub_cmds[i + 1]
                i += 2
                if cvals["LOAD"] == param:
                    # Value unchanged, nothing to do
                    break
                cvals["LOAD"] = param
                if param == "50":
                    # Derivative values
                    cvals["AMP"] = util.div(n=cvals["AMP"], d="2")
                    cvals["AMPVRMS"] = util.div(n=cvals["AMPVRMS"], d="2")
                    cvals["AMPDBM"] = util.div(n=cvals["AMPDBM"], d="2")
                    cvals["HLEV"] = util.div(n=cvals["HLEV"], d="2")
                    cvals["LLEV"] = util.div(n=cvals["LLEV"], d="2")
                elif param == "HZ":
                    # Derivative values
                    cvals["AMP"] = util.mul(a=cvals["AMP"], b="2")
                    cvals["AMPVRMS"] = util.mul(a=cvals["AMPVRMS"], b="2")
                    cvals["AMPDBM"] = util.mul(a=cvals["AMPDBM"], b="2")
                    cvals["HLEV"] = util.mul(a=cvals["HLEV"], b="2")
                    cvals["LLEV"] = util.mul(a=cvals["LLEV"], b="2")
                else:
                    return ""
                break

            for key in self.cvals:
                if cmd == key:
                    param = sub_cmds[i + 1]
                    cvals[key] = param
                    i += 2
                    break
            else:
                # This cmd is not suported
                errlog.error("Unknown sub_command '%s' in command '%s'", cmd, command)
                return ""

        return ""

    @abstractmethod
    def bswv(self, command: str) -> str:
        """Proccess all variants of the BSWV command."""
        cvals = self.cvals

        if command == "BSWV?":
            if cvals["LOAD"] == "50":
                return f"C{self.channel}:BSWV WVTP,{cvals['WVTP']},FRQ,{cvals['FRQ']}HZ,PERI,{cvals['PERI']}S,AMP,{cvals['AMP']}V,AMPVRMS,{cvals['AMPVRMS']}Vrms,AMPDBM,{cvals['AMPDBM']}dBm,OFST,{cvals['OFST']}V,HLEV,{cvals['HLEV']}V,LLEV,{cvals['LLEV']}V,PHSE,{cvals['PHSE']}"
            return f"C{self.channel}:BSWV WVTP,{cvals['WVTP']},FRQ,{cvals['FRQ']}HZ,PERI,{cvals['PERI']}S,AMP,{cvals['AMP']}V,AMPVRMS,{cvals['AMPVRMS']}Vrms,OFST,{cvals['OFST']}V,HLEV,{cvals['HLEV']}V,LLEV,{cvals['LLEV']}V,PHSE,{cvals['PHSE']}"

        if not command.startswith("BSWV "):
            errlog.error("Unknown command format: '%s'", command)
            return ""

        # Process the command (e.g., 'C1:BSWV FRQ,12')
        sub_cmds = command.split(" ")
        sub_cmds = sub_cmds[1].split(",")
        cmd = sub_cmds[0]

        if cmd == "FRQ":
            param = sub_cmds[1]
            cvals[cmd] = f"{float(param):g}"
            cvals["PERI"] = util.div(n="1", d=param)

        elif cmd == "AMP":
            param = sub_cmds[1]
            amp = float(param)
            # The function generator clamps the amplitude
            amp = max(amp, 0.002)
            amp = min(amp, 20)
            cvals["AMP"] = util.float_to_str(amp)
            # Vrms = Vpp * 1/sqrt(2) / 2 = Vpp * .3535
            cvals["AMPVRMS"] = util.mul(a=cvals["AMP"], b=".3535")
            cvals["HLEV"] = util.div(n=cvals["AMP"], d="2")
            cvals["LLEV"] = util.sub(a=cvals["HLEV"], b=cvals["AMP"])

        else:
            for key in self.cvals:
                if cmd == key:
                    param = sub_cmds[1]
                    cvals[key] = param
                    break
            else:
                # This cmd is not suported
                errlog.error("Invalid sub_command '%s' in command '%s'", cmd, command)
                return ""

        return ""

    def reset(self) -> str:
        """Reset the channel to defaults."""
        self.cvals = channel_defaults.copy()
        return ""

    def process(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        if not command.startswith(f"C{self.channel}:"):
            return ""

        sub_command = command[3:]

        if sub_command.startswith("OUTP"):
            return self.outp(command=sub_command)

        if sub_command.startswith("BSWV"):
            return self.bswv(command=sub_command)

        return ""


device_defaults: Dict[str, str] = {
    "CHDR": "SHORT",
    "BUZZ": "ON",
    "STL": "STL M10, ExpFal, M100, ECG14, M101, ECG15, M102, LFPulse, M103, Tens1, M104, Tens2, M105, Tens3, M106, Airy, M107, Besselj, M108, Bessely, M109, Dirichlet, M11, ExpRise, M110, Erf, M111, Erfc, M112, ErfcInv, M113, ErfInv, M114, Laguerre, M115, Legend, M116, Versiera, M117, Weibull, M118, LogNormal, M119, Laplace, M12, LogFall, M120, Maxwell, M121, Rayleigh, M122, Cauchy, M123, CosH, M124, CosInt, M125, CotH, M126, CscH, M127, SecH, M128, SinH, M129, SinInt, M13, LogRise, M130, TanH, M131, ACosH, M132, ASecH, M133, ASinH, M134, ATanH, M135, ACsch, M136, ACoth, M137, Bartlett, M138, BohmanWin, M139, ChebWin, M14, Sqrt, M140, FlattopWin, M141, ParzenWin, M142, TaylorWin, M143, TukeyWin, M144, Duty01, M145, Duty02, M146, Duty04, M147, Duty06, M148, Duty08, M149, Duty10, M15, Root3, M150, Duty12, M151, Duty14, M152, Duty16, M153, Duty18, M154, Duty20, M155, Duty22, M156, Duty24, M157, Duty26, M158, Duty28, M159, Duty30, M16, X^2, M160, Duty32, M161, Duty34, M162, Duty36, M163, Duty38, M164, Duty40, M165, Duty42, M166, Duty44, M167, Duty46, M168, Duty48, M169, Duty50, M17, X^3, M170, Duty52, M171, Duty54, M172, Duty56, M173, Duty58, M174, Duty60, M175, Duty62, M176, Duty64, M177, Duty66, M178, Duty68, M179, Duty70, M18, Sinc, M180, Duty72, M181, Duty74, M182, Duty76, M183, Duty78, M184, Duty80, M185, Duty82, M186, Duty84, M187, Duty86, M188, Duty88, M189, Duty90, M19, Gaussian, M190, Duty92, M191, Duty94, M192, Duty96, M193, Duty98, M194, Duty99, M195, demo1_375, M196, demo1_16k, M197, demo2_3k, M198, demo2_16k, M2, StairUp, M20, Dlorentz, M21, Haversine, M22, Lorentz, M23, Gauspuls, M24, Gmonopuls, M25, Tripuls, M26, Cardiac, M27, Quake, M28, Chirp, M29, Twotone, M3, StairDn, M30, SNR, M31, Hamming, M32, Hanning, M33, kaiser, M34, Blackman, M35, Gausswin, M36, Triangle, M37, BlackmanH, M38, Bartlett-Hann, M39, Tan, M4, StairUD, M40, Cot, M41, Sec, M42, Csc, M43, Asin, M44, Acos, M45, Atan, M46, Acot, M47, Square, M48, SineTra, M49, SineVer, M5, Ppulse, M50, AmpALT, M51, AttALT, M52, RoundHalf, M53, RoundsPM, M54, BlaseiWave, M55, DampedOsc, M56, SwingOsc, M57, Discharge, M58, Pahcur, M59, Combin, M6, Npulse, M60, SCR, M61, Butterworth, M62, Chebyshev1, M63, Chebyshev2, M64, TV, M65, Voice, M66, Surge, M67, Radar, M68, Ripple, M69, Gamma, M7, Trapezia, M70, StepResp, M71, BandLimited, M72, CPulse, M73, CWPulse, M74, GateVibr, M75, LFMPulse, M76, MCNoise, M77, AM, M78, FM, M79, PFM, M8, Upramp, M80, PM, M81, PWM, M82, EOG, M83, EEG, M84, EMG, M85, Pulseilogram, M86, ResSpeed, M87, ECG1, M88, ECG2, M89, ECG3, M9, Dnramp, M90, ECG4, M91, ECG5, M92, ECG6, M93, ECG7, M94, ECG8, M95, ECG9, M96, ECG10, M97, ECG11, M98, ECG12, M99, ECG13",
    "STL USER": "STL WVNM",
}


class SDG(ABC):
    """Emulate a Siglent SDG series function generator.

    There are several models in the Siglent family. Some support commands that
    others do not. For instance, not all support the CHDR command. This base
    class implements all common functionality and provides abstract methods for
    derived classes to implement specific functions.
    """

    channels: List[SDGChannel]
    dvals = device_defaults.copy()

    @abstractmethod
    def identification(self) -> str:
        """Process the command, update state, optionally return a result."""

    def operation_complete(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        if command == "*OPC?":
            # Format 1
            return "*OPC 1"
        return ""

    def reset(self) -> str:
        """Process the command, update state, optionally return a result."""
        self.dvals = device_defaults.copy()
        for channel in self.channels:
            channel.reset()
        return ""

    def comm_header(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        if command == "CHDR?":
            return f"CHDR {self.dvals['CHDR']}"
        params = command.split(" ")
        if len(params) < 2 or len(params) > 2:
            return ""
        if params[1] not in ["SHORT", "LONG", "OFF"]:
            return ""
        self.dvals["CHDR"] = params[1]
        return ""

    def parameter_copy(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        try:
            # Command is of the form 'PACP C2,C1'
            params = command.split(" ")
            if len(params) < 2 or len(params) > 2:
                return ""
            params = params[1].split(",")
            if len(params) < 2 or len(params) > 2:
                return ""
            dest = util.channel_to_index(channel=params[0])
            source = util.channel_to_index(channel=params[1])
        except Exception as err:
            errlog.exception(err)
            return ""
        self.channels[dest].cvals = self.channels[source].cvals.copy()
        return ""

    def store_list(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        if command == "STL?":
            return self.dvals["STL"]
        params = command.split(" ")
        if len(params) < 2 or len(params) > 2:
            return ""
        if params[1] == "BUILDIN":
            return self.dvals["STL"]
        if params[1] == "USER":
            return self.dvals["STL USER"]
        return ""

    def buzz(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        if command == "BUZZ?":
            return f"BUZZ {self.dvals['BUZZ']}"
        params = command.split(" ")
        if len(params) < 2 or len(params) > 2:
            return ""
        if params[1] not in ["ON", "OFF"]:
            return ""
        self.dvals["BUZZ"] = params[1]
        return ""

    # pylint: disable=too-many-return-statements
    def dispatch(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        command = util.shorten_verbs(command)

        # Is this a device command?
        if command == "*IDN?":
            return self.identification()
        if command.startswith("*OPC"):
            return self.operation_complete(command=command)
        if command.startswith("PACP"):
            return self.parameter_copy(command=command)
        if command == "*RST":
            return self.reset()
        if command.startswith("CHDR"):
            return self.buzz(command=command)
        if command.startswith("BUZZ"):
            return self.buzz(command=command)
        if command.startswith("STL"):
            return self.store_list(command=command)

        # Is this is a channel command?
        if re.match("C[1-2]:", command):
            try:
                channel = int(command[1])
            except Exception as err:
                errlog.exception(err)
                return ""
            channel -= 1
            if channel < 0 or channel >= len(self.channels):
                return ""
            return self.channels[channel].dispatch(command=command)

        # This was not a valid command
        return ""

    def process(self, command: str) -> str:
        """Normalize the command to the short version as it comes in and to the CHDR-specified format as it goes out."""
        command = util.shorten_verbs(command)
        response = self.dispatch(command)
        return util.format_verbs(response, self.dvals["CHDR"])


errlog = logging.getLogger(__name__)
