from modules.abstract.scanner import Scanner
from modules.logger import logger
from modules.scanner.finding import Finding
from modules.scanner import ScannerManager
import lief


@ScannerManager.add_mimetype_scanner('application/x-mach-binary')
class BinaryScanner(Scanner):
    async def perform_scan(self):
        binary = lief.parse(self.file_to_scane)
        if binary.header.file_type == lief.MachO.FILE_TYPES.EXECUTE:
            no_pie = True
            allow_stack_execution = False
            for flag in binary.header.flags_list:
                if flag == lief.MachO.HEADER_FLAGS.PIE:
                    no_pie = False
                if flag == lief.MachO.HEADER_FLAGS.ALLOW_STACK_EXECUTION:
                    allow_stack_execution = True

            if no_pie:
                await self.report.add_finding(
                    Finding(
                        title='No PIE protection',
                        description='Position Independent Executables (PIE) are an output of the hardened package build'
                                    'process. A PIE binary and all of its dependencies are loaded into random locations'
                                    'within virtual memory each time the application is executed. This makes Return '
                                    'Oriented Programming (ROP) attacks much more difficult to execute reliably.'
                                    f'Scanner detect that the {self.file_to_scan} binary does not have PIE protection.',
                        likelihood=1,
                        impact=1,
                        risk=1,
                        recommendation='Please implement PIE protection on the binary to make ROP attack more '
                                       'difficult to perform.'

                    )
                )

                if allow_stack_execution:
                    await self.report.add_finding(
                        Finding(
                            title='Vulnerable to stack buffer overflow',
                            description='Stack based buffer overflow occurs when a program writes to a memory address '
                                        'on the program\'s call stack outside of the intended data structure, '
                                        'which is usually a fixed-length buffer. One of many protections against this '
                                        'attack is to implement NX. Non-Executable (NX) memory in simple terms is a '
                                        'part of the memory in which if someone tries to inject the machine code, '
                                        f'it won\'t let that happen. Scanner detect that the {self.file_to_scan} '
                                        'binary does not have NX protection.',
                            likelihood=1,
                            impact=4,
                            risk=3,
                            recommendation='Please implement NX flag on the stack to prevent buffer overflow attack.'
                        )
                    )

                    no_objc_release = True
                    no_swift_release = True
                    for symbol in binary.symbols:
                        if symbol.name == '_objc_release':
                            no_objc_release = False
                        elif symbol.name == '_swift_release':
                            no_swift_release = False

                    if no_objc_release and no_swift_release:
                        await self.report.add_finding(
                            Finding(
                                title='No ARC protection',
                                description='Automatic Reference Counting (ARC) is a memory management feature of the '
                                            'Clang compiler providing automatic reference counting for the '
                                            'Objective-C and Swift programming languages. At compile time, '
                                            'it inserts into the object code messages retain and release which '
                                            'increase and decrease the reference count at run time, marking for '
                                            'de-allocation those objects when the number of references to '
                                            'them reaches zero. Scanner detect that the {self.file_to_scan} binary '
                                            'does not have ARC protection.',
                                likelihood=1,
                                impact=1,
                                risk=1,
                                recommendation='Please implement ARC to prevent memory leaks.'
                            )
                        )
                    commands = list(map(lambda x: x.command, binary.commands))
                    if lief.MachO.LOAD_COMMAND_TYPES.ENCRYPTION_INFO not in commands and lief.MachO.LOAD_COMMAND_TYPES.ENCRYPTION_INFO_64 not in commands:
                        await self.report.add_finding(
                            Finding(
                                title='Binary file is not encrypted',
                                description='App Store binaries are signed by both their developer and Apple. This '
                                            'encrypts the binary so that decryption keys are needed in order to make '
                                            'the binary readable. When iOS executes the binary, the decryption keys '
                                            'are used to decrypt the binary into a readable state where it is then '
                                            'loaded into memory and executed. iOS can tell the encryption status of a '
                                            'binary via the cryptid struture member of LC_ENCRYPTION_INFO MachO load '
                                            f'command. Scanner detect that the {self.file_to_scan} binary does not '
                                            'encrypted.',
                                likelihood=1,
                                impact=1,
                                risk=1,
                                recommendation='Please implement binary encryption to make reverse engineering and '
                                               'static analysis harder to perform. '
                            )
                        )
