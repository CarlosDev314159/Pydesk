from tkinter import Tk, messagebox, filedialog
import time, os, webbrowser, psutil, subprocess, random, string, sys
from colorama import init
import json, distro
from colorama import Fore
from notifypy import Notify
# importing libs


# Initialize the colorama module and autoreset the colors in end of the line
# Inicializar o módulo colorama e autoreseta as cores no final da linha
init(autoreset=True)


# configuration class 

class Configuration:
    def __init__(self):
        self.message = Notification(Tk)
        self.message._dialogbox.withdraw()

        # Cria um dicionário de configurações com os valores atuais lidos do arquivo JSON
        self.config = {1: {"Remove unused packages": self.showPreference(key="Config", value="Remove unused packages")},
                       2: {"Use the OS information to do Google searches": self.showPreference(key="Config", value="Use OS information to perform Google searches")}
                    }
  

    def showPreference(self, key, value):
        # Lê o arquivo JSON de preferências e retorna o valor da preferência especificada
        with open("config/preferences.json", "r") as preference:
            data = json.load(preference)
            return data[key][value]
    

    def changePreferences(self, title, message, key, value):
        # Abre o arquivo JSON de preferências e altera o valor da preferência especificada
            with open("config/preferences.json", "r") as preferences:
                data = json.load(preferences)

                # Se o valor da preferência for "False", exibe uma caixa de diálogo e altera o valor para "True" se confirmado
                if data[key][value] == "False":
                    help_box = self.message.showHelp(title, message)
                    if not(help_box):
                        pass
                    else:
                        data[key][value] = "True"
                        with open("config/preferences.json", "w") as preferences:
                            json.dump(data, preferences, indent=2)

            # Se o valor da preferência for "Disabled", altera para "Activated" e exibe uma caixa de diálogo de confirmação
            with open("config/preferences.json", 'r') as preferences:
                data = json.load(preferences)
                if data[key][value] == "Disabled":
                    with open("config/preferences.json", "w") as preferences:
                        data[key][value] = "Activated"
                        json.dump(data, preferences, indent=2)
                    help_box = self.message.popUp(title, message, "images/settings.png")
                    if not(help_box):
                        pass

                # Se o valor da preferência for "Activated", altera para "Disabled" e exibe uma caixa de diálogo de confirmação    
                elif data[key][value] == "Activated":
                    with open("config/preferences.json", "w") as preferences:
                        data[key][value] = "Disabled"
                        json.dump(data, preferences, indent=2)
                    changed = self.message.popUp("Configuration", "Your preference has been successfully changed!", "images/settings.png")
                    return changed
                
    
    def seeConfig(self, value):
        # Abre o arquivo JSON de preferências e lê o valor da configuração especificada
        with open("config/preferences.json", "r") as preferences:
            data = json.load(preferences)
        # Retorna False se o valor da configuração for "Disabled", True caso contrário
        if data["Config"][value] == "Disabled":
            return False
        else:
            return True


    def configControl(self):
        title = "Configurations"
        print('\033[1m', "-" * 64, '\033[0m')
        print('\033[1m', title.center(64), '\033[0m')
        print('\033[1m', "-" * 64, '\033[0m')

        # Lê as configurações atuais do arquivo JSON e as armazena no dicionário self.config
        self.config = {1: {"Remove unused packages": self.showPreference("Config", "Remove unused packages")}, 2: {"Use OS information to perform Google searches": self.showPreference("Config", "Use OS information to perform Google searches")}}
        
        # Exibe as configurações na tela
        print(f"[1]Remove unused packages -> {self.config[1]['Remove unused packages']}\n")
        print(f"[2]Use OS information to perform Google searches -> {self.config[2]['Use OS information to perform Google searches']}\n")
        
        try:
            # Solicita que o usuário insira o número da opção desejada
            print("Press '0' to back to menu\n")
            option = int(input("Choose an option you want to change: "))
            print("\n")
            # Verifica se a opção escolhida é válida e altera o valor da configuração especificada
            if option == 1:
                self.changePreferences("Configuration", 
                "Your preference has been successfully changed!",
                 "Config",
                 "Remove unused packages"
                )
                self.configControl()
            elif option == 2:
                self.changePreferences("Configuration", 
                "Your preference has been successfully changed!",
                 "Config",
                 "Use OS information to perform Google searches"
                )
                self.configControl()
            elif option > 2:
                # Exibe uma mensagem de erro se a opção for inválida
                self.message.showError(title="Option Invalid", message="Oops, that option doesn't exist!")
                print(Fore.RED + "Error")
                
                self.configControl()
            else:
               # Retorna ao menu principal se o usuário inserir o número "0"
               Main.menu()
        except ValueError as e:
            # Exibe uma mensagem de erro se o usuário inserir um valor não numérico
            self.message.showError(title="Error", message="Oops, choose an amount in numbers, let's try again.")
            print(Fore.RED + "Error" + "Error log: " + e)
            
            self.configControl()


       #end configuration class


  #start notification class
class Notification:
    def __init__(self, tk):
        self._dialogbox = Tk()
        self._dialogbox.withdraw()
        self._popup = Notify()
        

    def showInfo(self, title, message):
        return messagebox.showinfo(title, message)

    def showWarning(self, title, message):
        return messagebox.showwarning(title, message)

    def showError(self, title, message):
        return messagebox.showerror(title, message)

    def showHelp(self, title, message):
        return messagebox.askokcancel(title, message)

    def showOptions(self, title, message):
        return messagebox.askyesno(title, message)

    def popUp(self, title, message, icon, duration=5):
        # Only use this method to show small texts and information, 
        # otherwise use the ones already defined above.

        self._popup.title = title
        self._popup.message = message
        self._popup.icon = icon
        self._popup.timeout = duration * 1000  # timeout is in milliseconds
        return self._popup.send()


    # end notification class


    # start  directory creator class
class DirectoryCreator(Notification):
    def __init__(self):
        self.message = Notification(Tk)
        self.help_message_directory = "Here you can create multiple directories in a fast and simple way."
        self.permission_error_message = "You don't have permission to access this directory, please choose another one."
    

    def handle_permission_error(self):
        self.message.showError("Permission Denied", self.permission_error_message)
        print(f"{Fore.RED}Error")
        return self.create_directories()

    def ask_amount_of_directories(self):
        try:
            return int(input("How much directories do you would like to create?\n"))
        except ValueError:
            self.message.showError(title="Error", message="Oops, choose an amount in numbers, let's try again.")
            print(Fore.RED + "Error")
            return self.ask_amount_of_directories()

    def read_directory_names(self):
        return [input("Type directory's name:\n") for _ in range(self.ask_amount_of_directories())]
    

    def generate_random_name(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
  

    def create_directories(self):
        Configuration().changePreferences("What this does?!", self.help_message_directory, "HelpDialogBox", "dirCreator_BoxHelp")

        place = filedialog.askdirectory(title="Where would you like to create?")
        if not place:
            print("\n")
            print(Fore.RED + " Canceled by user")
            print("\n")
            return Main.menu()

        path = place
        os.chdir(path)
        print(f"\n{Fore.BLUE}If you don't want to name your directories now, just press {Fore.GREEN} Enter {Fore.BLUE} to create random names \n")
        for dirname in self.read_directory_names():
            try:
                if dirname == "":
                    dirname = self.generate_random_name()
                    command = os.system(f"mkdir {dirname}")
                else:
                    command = os.system(f"mkdir {dirname.replace(' ', '_')}")
                if command == 25600:
                    self.handle_permission_error()
                    return Main.menu()
            except PermissionError:
                self.handle_permission_error()
            except Exception as e:
                self.message.showError(title="Error", message="Oops, something went wrong")
                print(Fore.RED + f"Error log: {e}\n")
        print("\n")
        return Main.menu()

    #end directory creator class


    #start system update class
class SystemUpdater(Notification):
    def __init__(self, remove_unused_packages=False):
        self.message = Notification(Tk)
        self.help_message_update = "Here you can update your computer quickly and easily without any bash lines."
        self.remove_unused_packages = remove_unused_packages
        self.show_option_message = "Do would you like to remove unused packages?"

    def ask_remove_unused_packages(self):
        try:
           answer = self.message.showOptions(title="A Question...", message=self.show_option_message)
           if answer:
                self.remove_unused_packages = True
        except Exception as err:
            self.message.showError(title="Error", message=err)
    
    
    def update(self):
        Configuration().changePreferences(title="What this does?!", message=self.help_message_update, key="HelpDialogBox", value="update_BoxHelp")
        self.print_title("Update the system")
        self.ask_remove_unused_packages()
        update_command = "sudo apt update && sudo apt full-upgrade -y"
        if self.remove_unused_packages:
            update_command = "sudo apt autoremove -y && " + update_command
        os.system(update_command)
        self.message.popUp("Successfully Updated", "Your computer is up to date!", "images/accept.png")
        time.sleep(0.5)
        return Main.menu()
    
    @staticmethod
    def print_title(title):
        print("\n")
        print('\033[1m', "-" * 64, '\033[0m')
        print('\033[1m', title.center(64), '\033[0m')
        print('\033[1m', "-" * 64, '\033[0m')

        
    
         #end system update class






        #start installer class
class Installer(Notification):
    def __init__(self):
        self.message = Notification(Tk)
        self.dist = distro.linux_distribution()

        # Mensagem de ajuda exibida quando o usuário solicita ajuda na tela de instalação

        self.help_message_installer = "Here you can install packages on your computer quickly and easily, without a bash command. If the package is not found, we will redirect you to Google to help you find and download it. By default, data from your operating system will not be sent to improve searches. but you can activate in the 'Configuration' option"
        
        # Mensagem de ajuda exibida quando o software solicitado não é encontrado no repositório de pacotes
        
        self.help_message_package = "Sorry, this software is not in your package repository, but don't worry! I will help you find it. let's redirect it to Google."

    # Lê a configuração "Use OS information to perform Google searches"
    config_args = Configuration().seeConfig("Use OS information to perform Google searches")


    def installer(self, use_os_info=config_args):
        Configuration().changePreferences("What this does?!", self.help_message_installer, "HelpDialogBox", "installer_BoxHelp")
        title = "Installer"
        print('\033[1m', "-" * 64, '\033[0m')
        print('\033[1m', title.center(64), '\033[0m')
        print('\033[1m', "-" * 64, '\033[0m')
       
        # Loop infinito para solicitar o valor de "amount" até que um valor válido seja digitado
        while True:
            try:
                # Solicita o número de softwares a serem instalados
                amount = int(input("How much software would you like to install?\n"))
                # Sai do loop quando um valor válido é digitado
                break
            except ValueError:
                # Exibe uma mensagem de erro e volta para o início do loop
                self.message.showError(title="Error", message="Oops, choose an amount in numbers, let's try again.")
                print(Fore.RED + "Error")
                
    # Loop para instalar o número de softwares solicitado pelo usuário
        
        for _ in range(amount):
            
            # Solicita o nome do software a ser instalado
            software_name = input("Type the software name:\n")
           
            # Instala o software com o comando "sudo apt install"
            install_command = os.system(f"sudo apt install {software_name}")
            
            # Verifica se o software foi encontrado no repositório de pacotes
            if install_command == 25600:
                # Exibe uma mensagem de erro e solicita ao usuário se deseja continuar ou voltar ao menu principal
                print(Fore.RED + "Error")
                warning_not_found = self.message.showHelp(title="This software isn't found", message=self.help_message_package)
                
                # Se o usuário escolheu voltar ao menu principal, retorna à função "menu"
                if not(warning_not_found):
                    print("\n")
                    print(Fore.RED + " Canceled by user")
                    print("\n")
                    return Main.menu() 
                # Se a configuração "Use OS information to perform Google searches"
                if use_os_info:
                    webbrowser.open(f"https://www.google.com/search?q=Download '{software_name}' for {self.dist[0]} {self.dist[1]}")
                else:
                    webbrowser.open(f"https://www.google.com/search?q=Download {software_name}")

        return Main.menu()

        #end installer class


class SwapModificator(Notification):
    def __init__(self):
        self.message = Notification(Tk)
        self.message._dialogbox.withdraw()
        self.help_message_swap = "Here you can make changes in a simple and intuitive way. Do you know what Swap is?\nThe swap space is located on disk, in the form of a partition or a file. Linux uses it to extend the memory available to processes, storing infrequently used pages there. We usually configure swap space during the operating system installation."
        self.error_message_swap = "Some error occurred when creating your swap file"
        self.total_memory = psutil.virtual_memory().total / 1024 ** 3
    
    def get_memory(self):
        # Exibe a quantidade de memória RAM já convertida em gigabytes
        total_memory = psutil.virtual_memory().total / 1024 ** 3
        avaliable_memory = psutil.virtual_memory().available / 1024 ** 3
        used_memory = psutil.virtual_memory().used / 1024 ** 3


        system_memory = {
            "title": "RAM:",
            "total":  total_memory,
            "available":  avaliable_memory,
            "used":  used_memory,
        }

        return(f"{system_memory['title']}\n"
                    f"Total: {round(system_memory['total'])}GB\n"
                    f"Free: {round(system_memory['available'])}GB\n"
                    f"Used: {round(system_memory['used'])}GB\n"
                )
    
    
    
    def show_paths(self, path_root="/", path_home="/home"):
        # Exibe os Paths de arquivos

        # Define os Paths
        disk_root = psutil.disk_usage(path=path_root)
        disk_home = psutil.disk_usage(path=path_home)


        # Path / -> root
        total_root = disk_root.total
        used_root = disk_root.used
        free_root = disk_root.free
        percent_root = disk_root.percent

        # Path /home -> home, se disponível
        total_home = disk_home.total
        used_home = disk_home.used
        free_home = disk_home.free
        percent_home = disk_home.percent

        system_root = {
            "path": path_root,
            "total": round((total_root / 1024**3)),
            "used": round((used_root / 1024**3)),
            "free": round((free_root / 1024**3)),
            "percent": percent_root
        }

        system_home = {
            "path": path_home,
            "total": round((total_home / 1024**3)),
            "used": round((used_home / 1024**3)),
            "free": round((free_home / 1024**3)),
            "percent": percent_home
        }
        

        if disk_home == disk_root:
            return (f"Path: {system_root['path']}\n"
                    f"Total: {system_root['total']}GB\n"
                    f"Used: {system_root['used']}GB\n"
                    f"Free: {system_root['free']}GB\n"
                    f"Usage percentage: {system_root['percent']}%\n")
        else:
            return (f"Path: {system_root['path']}\n"
                    f"Total: {system_root['total']}GB\n"
                    f"Used: {system_root['used']}GB\n"
                    f"Free: {system_root['free']}GB\n"
                    f"Usage percentage: {system_root['percent']}%\n\n"

                    f"Path: {system_home['path']}\n"
                    f"Total: {system_home['total']}GB\n"
                    f"Used: {system_home['used']}GB\n"
                    f"Free: {system_home['free']}GB\n"
                    f"Usage percentage: {system_home['percent']}%\n\n"

                    f"{self.get_memory()}\n"
            )
            

    def create_swap_file(self, gigabytes):
        # Cria o arquivo de swap com o tamanho especificado em gigabytes
        try:
            subprocess.call(["sudo", "fallocate", "-l", f"{gigabytes}G", "/swapfile"])
            subprocess.call(["sudo", "chmod", "600", "/swapfile"])
            subprocess.call(["sudo", "mkswap", "/swapfile"])
            subprocess.call(["sudo", "swapon", "/swapfile"])
            result = subprocess.call(["sudo", "swapon", "--show"])
            if result == 0:
                self.message.showInfo(title="Sucess", message="Swap file created sucessufuly")
            else:
                self.message.showError(title="Error", message=self.error_message_swap)
            return Main.menu()
        except Exception as e:
            self.message.showError("Error", self.error_message_swap)
            print(f"\n{Fore.RED}Error log: {e}")
            return Main.menu()

    def disable_swap(self):
        # Desativa o arquivo de swap
        try:
            subprocess.call(["sudo", "swapoff", "-a"])
            subprocess.call(["sudo", "rm", "/swapfile"])
        except Exception as e:
            self.message.showError("Error", self.error_message_swap)
            print(f"{Fore.YELLOW}Error log: {e}")
            return Main.menu()

    def get_swap_status(self):
        # Verifica se o arquivo de swap está ativo
        result = subprocess.run(["sudo", "swapon", "--show"], stdout=subprocess.PIPE)
        return "SIZE" in result.stdout.decode()

    def swap_modificator(self):
        # Inicializa o modificador de swap
        Configuration().changePreferences("What this does?!", self.help_message_swap, "HelpDialogBox", "swap_BoxHelp")
        title = "Swap Modificator"
        print('-' * 64)
        print(title.center(64))
        print('-' * 64)

        # Exibe os caminhos de arquivos
        try:
            print(self.show_paths())
        except FileNotFoundError as e:
            error_log = f"Error log: {e}"
            self.message.showError(title="Error", message=error_log)
            return Main.menu()

        print(f"{Fore.YELLOW}Warning: You must be root to use this option\n")

        # Verifica se o arquivo de swap está ativo
        if self.get_swap_status():
            # Pergunta ao usuário se deseja sobrescrever o arquivo de swap existente
            response = self.message.showHelp("Swap Modificator", "You already have a swap file on your computer, do you want to overwrite it?")
            if not response:
                print(f"\n{Fore.RED}Canceled by user\n")
                return Main.menu()
            else:
                # Desativa o arquivo de swap
                try:
                    self.disable_swap()
                except Exception as e:
                    self.message.showError("Error", "Failed to disable swap file")
                    print(f"Error log: {e}")
                    return Main.menu()
        else:
            try:# Pergunta ao usuário quantos gigabytes deseja adicionar ao arquivo de swap
                gigabytes = int(input("How many gigabytes would you like to add to swap?\n"))
                if gigabytes < self.total_memory / 2:
                    self.message.showWarning("Invalid value", "Invalid length value specified,\nThe value in gigabytes should be close to the amount of RAM in your operating system.")
                    print(f"{Fore.YELLOW}\nWarning log: Invalid length value specified\n")
                    return self.swap_modificator()
            except ValueError as e:
                self.message.showWarning("Invalid value", "Invalid length value specified,\nOnly values of the type integer are allowed.")
                print(f"{Fore.RED}Error log: {e}\n")
                return Main.menu()

            # Cria o arquivo de swap
            self.create_swap_file(gigabytes)

            # Fim da classe SwapModificator


class Main:
    
    @classmethod
    def menu(self):
        title = "PyDesk v0.1"
        print('\033[1m', Fore.YELLOW + "-" * 64, '\033[0m')
        print('\033[1m', title.center(64), '\033[0m')
        print('\033[1m', Fore.BLUE + "-" * 64, '\033[0m')
     

         # Lê a opção do usuário
        try:
            option = int(input(
                "[1]Update\n[2]Installer\n[3]Directory Creator\n[4]Swap Modificator\n[5]Configuration\n[6]Report a bug\n[7]Exit\nChoose a option: "))
        except ValueError:
            print(f"\n{Fore.YELLOW}Option not found! Please choose a valid option.\n")
            return self.menu()
        except (KeyboardInterrupt, InterruptedError, EOFError):
            print(f"\n{Fore.RED}Cancelled by user.\n")
            return sys.exit(1)
        except FileNotFoundError as e:
            Notification(Tk).showError("Error", "Oops, something went wrong, the file 'preferences.json' was not found, please check if it exists, if you consider this to be a bug, please report it!")
            print(f"\n{Fore.RED}Error log: {e}\n")
            return self.menu()


        # Instanciando as classes
        var_system_updater = SystemUpdater()
        var_installer = Installer()
        var_directory_creator = DirectoryCreator()
        var_swap_modificator = SwapModificator()
        var_configuration = Configuration()

        # Executa a opção selecionada pelo usuário
        if option == 1:
            var_system_updater.update()
        elif option == 2:
            var_installer.installer()
        elif option == 3:
            var_directory_creator.create_directories()
        elif option == 4:
            var_swap_modificator.swap_modificator()
        elif option == 5:
            var_configuration.configControl()
        elif option == 6:
            webbrowser.open("https://github.com/CarlosDev314159/Pydesk/issues")
            print(f"\n{Fore.GREEN}Thanks for your report!\n")
            Notification(Tk).popUp("Report a Bug", "Thanks for your report!", "images/bug-report.png")
            return self.menu()
        elif option == 7:
                sys.exit()
        else:
            Notification(Tk).showError("Error", "Option not found! Please choose a valid option.")
            print(Fore.RED + "Error")
            return self.menu()
    

# Start the application
app = Main()
app.menu()
