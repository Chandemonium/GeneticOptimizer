#!/usr/bin/python

import os
import sys
import numpy as np
import subprocess
import time
import threading
import random

class GeneticOptimizer():
    def __init__(self):
        self.parameters_random = []
        self.parameters_7 = []

    def TrulyRandomNumbers(self, num):
        x = self.parameters_random
        print(x)
        for i in range(0,num):
            x.append(np.random.uniform(0.0,2.0))
        print(x)
        
        return x

    def SevenRandomNumbers(self):
        x = self.parameters_7
        print(x)
        # Cos
        x.append(np.random.uniform(0.5,2.0))
        #Css
        x.append(np.random.uniform(0.0, 1.0))
        # S8
        x.append(np.random.uniform(0.5,2.0))
        # a1
        x.append(np.random.uniform(0.0,2.0))
        # a2
        x.append(np.random.uniform(-1.0,1.0))
        # rcut
        x.append(np.random.uniform(0.0,1.5))
        # w 
        x.append(np.random.uniform(0.5,2.0))


        print(x)
        return x


    def MakeParamOptFile(self, params, number, generation):
        Number = str(number)
        Template = "Template.yaml"
        filename = "P_" + Number + ".yaml"
        output = "P_" +  Number + ".out"
        o = open(output, 'w')
        o.close()
        Command = ["cp", Template, filename]
        subprocess.Popen(Command, stdout=subprocess.PIPE)
        time.sleep(0.2)

        p1 = "x0: " + str(params[0])
        p2 = "x1: " + str(params[1])
        p3 = "d3_s8: " + str(params[2])
        p4 = "d3_a1: " + str(params[3])
        p5 = "d3_a2: " + str(params[4])
        p6 = "development->:d3_double_damping_r: " + str(params[5])
        p7 = "development->:d3_double_damping_w: " + str(params[6])

        p = [p1,p2,p3,p4,p5,p6,p7]
        Text = ["x0: param_1", "x1: param_2", "d3_s8: param_3", "d3_a1: param_4", "d3_a2: param_5", "development->:d3_double_damping_r: param_6", "development->:d3_double_damping_w: param_7"]

        # Loop through the new inputs, and write in the new parameters
        for i in range(0,7):

            f = open(filename,'r')
            filedata = f.read()
            f.close()

            PARAM = filedata.replace(Text[i], p[i])
            f = open(filename,'w')
            f.write(PARAM)
            f.close()
  
            # Create a directory for the current generation, and move all the parameter.yaml files into it
        Directory = generation
        Command2 = ["mv", filename, output, Directory]
        subprocess.Popen(Command2, stdout=subprocess.PIPE)
        Command3 = ["cp", "uchf_unrest_mod.yaml", Directory]
        subprocess.Popen(Command3, stdout=subprocess.PIPE)
        Command4 = ["cd", Directory]
        subprocess.Popen(Command4, stdout=subprocess.PIPE)
        Command5 = ["cuby4", filename, output]
        new_filename = Directory + "/" + filename
        new_output = Directory + "/" + output
        time.sleep(0.2)
        #create the Cuby4 command
        Command5 = "cuby4 " + new_filename + " > " + new_output

        return Command5

    def MutateSCSParameters(self,params):
        length = len(params)
        mutated_params = []
        counter = 0
        x_0 = [np.random.uniform(0.5,2.0) for i in range(0,length)]
        x_1 = [np.random.uniform(0.0,1.0) for i in range(0,length)]
        for i in range(0,length):
            mutated_params.append(counter)
            
            tmp_param = params[i]
            cos = x_0[i]
            css = x_1[i]
            tmp_param[0] = cos
            tmp_param[1] = css

            mutated_params[counter] = tmp_param
            counter += 1

        return mutated_params

    # This function mutates the pair a1 and a2 simultaneously
    def MutateDampingParameters(self,params):
        length = len(params)
        mutated_params = []
        counter = 0
        # A list with 5 random a1 values
        x_3 = [np.random.uniform(0.0,2.0) for i in range(0,length)]
        # A list with 5 random a2 values
        x_4 = [np.random.uniform(-1.0,1.0) for i in range(0,length)]
        for i in range(0,length):
            mutated_params.append(counter)
            

            tmp_param = params[i]
            a1 = x_3[i]
            a2 = x_4[i]
            tmp_param[3] = a1
            tmp_param[4] = a2

            mutated_params[i] = tmp_param
            counter += 1
        return mutated_params

    # This function mutates the s8 parameter
    def MutateS8Parameter(self,params):
        length = len(params)
        mutated_params = []
        counter = 0
        # A list with 5 random s8 values
        x_2 = [np.random.uniform(0.5,2.0) for i in range(0,length)]

        for i in range(0,length):
            mutated_params.append(counter)

            tmp_param = params[i]
            s8 = x_2[i]
            tmp_param[2] = s8

            mutated_params[i] = tmp_param
            counter += 1
        return mutated_params

    # This function creates new parameter sets with inherited traits from previous generations
    def InheritTraits(self,params):
        length = len(params)
        inherited_populations = []
        counter = 0
        for i in range(0,length):
            inherited_populations.append(counter)
            parent_1 = random.choice(params)
            parent_2 = random.choice(params)

            c = parent_1 + parent_2
            random.shuffle(c)
            new_params = c[:len(parent_1)]
            inherited_populations[i] = new_params
            counter += 1
        return inherited_populations





def call_script(*args):
    w = subprocess.Popen(args,shell=True)
    w.communicate()

def main():

    cwd = str(os.getcwd())
    All_Errors = []
    All_Generations = []
    best_params = []

    
    for f in range(0,int(sys.argv[1])):
        Params = []
        ERRORS = []
        Files = []
        counter = 0
        Generation = str(f)
        current_path = cwd + "/"  + Generation
        Command = ["mkdir", Generation]
        subprocess.Popen(Command, stdout=subprocess.PIPE)
        Threads = []
        if (f==0):
            for i in range(0,int(sys.argv[2])):
                Threads.append(i)
                GO = GeneticOptimizer()
                RN = GO.SevenRandomNumbers()
   
                command = GO.MakeParamOptFile(RN, i, Generation)
                T = threading.Thread(target=call_script, args=(command,))
                Threads[i] = T

            for x in Threads:
                x.start()
            for x in Threads:
                x.join()
                del x

            for filename in sorted(os.listdir(current_path)):


                if filename.endswith(".out"):
                    associated_params = [0.0 for i in range(0,7)]
                    new_filename = current_path + "/" + filename

                    command = ['grep', "Error:", new_filename]
                    
                    grep = subprocess.Popen(command, stdout=subprocess.PIPE)
                    # output stores the final error from the optimization file
                    output = subprocess.check_output(('tail', '-1'), stdin=grep.stdout)

                    if len(output) !=0:
                        output = output.split()[1]
                    else:
                        output = 100.0
                    ERRORS.append(counter)
                    Files.append(counter)
                    Params.append(counter)
                    ERRORS[counter] = output
                    Files[counter] = filename

                    
                    # grab the Cos coefficient from the output file
                    command2 = ['grep', "x0:", new_filename]
                    
                    grep = subprocess.Popen(command2, stdout=subprocess.PIPE)
                    # output stores the final Cos parameter
                    output2 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    if len(output2) !=0:
                        output2 = output2.split()[1]
                    else:
                        output2 = 0.0

                    associated_params[0] = output2

                    # grab the Css coefficient from the output file
                    command3 = ['grep', "x1:", new_filename]
                    
                    grep = subprocess.Popen(command3, stdout=subprocess.PIPE)
                    # output stores the final Css parameter
                    output3 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    if len(output3) !=0:
                        output3 = output3.split()[1]
                    else:
                        output3 = 0.0
                    associated_params[1] = output3

                    # grab the S8 coefficient from the output file
                    command4 = ['grep', "d3_s8:", new_filename]
                    
                    grep = subprocess.Popen(command4, stdout=subprocess.PIPE)
                    # output stores the final s8 parameter
                    output4 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    if len(output4) !=0:
                        output4 = output4.split()[1]
                    else:
                        output4 = 0.0
                    associated_params[2] = output4

                    # grab the a1 coefficient from the output file
                    command5 = ['grep', "d3_a1:", new_filename]
                    
                    grep = subprocess.Popen(command5, stdout=subprocess.PIPE)
                    # output stores the final a1 parameter
                    output5 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    if len(output5) !=0:
                        output5 = output5.split()[1]
                    else:
                        output5 = 0.0
                    associated_params[3] = output5

                    # grab the a2 coefficient from the output file
                    command6 = ['grep', "d3_a2:", new_filename]
                    
                    grep = subprocess.Popen(command6, stdout=subprocess.PIPE)
                    # output stores the final a2 parameter
                    output6 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    if len(output6) !=0:
                        output6 = output6.split()[1]
                    else:
                        output6 = 0.0
                    associated_params[4] = output6

                    # grab the rcut coefficient from the output file
                    command7 = ['grep', ":d3_double_damping_r", new_filename]
                    dashout = subprocess.Popen(command, stdout=subprocess.PIPE)
                    grep = subprocess.Popen(command7, stdout=subprocess.PIPE)
                    # output stores the final rcut parameter
                    output7 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    if len(output7) !=0:
                        output7 = output7.split()[2]
                    else:
                        output7 = 0.0
                    associated_params[5] = output7

                    # grab the width coefficient from the output file
                    command8 = ['grep', ":d3_double_damping_w", new_filename]
                    
                    grep = subprocess.Popen(command8, stdout=subprocess.PIPE)
                    # output stores the final width parameter
                    output8 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    if len(output8) !=0:
                        output8 = output8.split()[2]
                    else:
                        output8 = 0.0
                    associated_params[6] = output8

                    Params[counter] = associated_params


                    counter += 1

    ### After the inital population
        del Threads
        Threads = []
        if (f>0):
            print("generation ",f)
            # top_performers is a deep copy of the best_params list. Lists are mutable in Python which means that the mutate and inherit functions were chaning my list copies and the original list object. A deep copy is a seperate object, so it can be changed without changing the original list.
            top_performers = [x[:] for x in best_params]
            print("best_params: ", best_params)
            print("top performers 1: ", top_performers)

            # I need this part of the code to loop over all subseqent generations


            object = GeneticOptimizer()


            # Create mutant populations

            mutants = object.MutateSCSParameters(top_performers)
            print("These are the spin coefficient mutants ", mutants)


            top_performers_2 = [x[:] for x in best_params]
            
            mutants_2 = object.MutateDampingParameters(top_performers_2)
            
            print("These are the damping parameter mutants ", mutants_2)

            # This is my new mutant that only mutates the s8 parameter
            top_performers_4 = [x[:] for x in best_params]
            mutants_3 = object.MutateS8Parameter(top_performers_4)
            print("These are the S8 parameter mutants ", mutants_3)


            # Create an inherited populations by shuffling the best performers
            top_performers_3 = [x[:] for x in best_params]
            inherited = object.InheritTraits(top_performers_3)
            print("These are the inherited parameters ", inherited)

            # These operators are not needed at this time

            # Inherit new Cos and Css for top performers
            #top_performers_3 = [x[:] for x in best_params]
            #inheritedspincoeffs = object.InheritSpinCoeffs(top_performers_3)
            #print("top performers 4: ", top_performers_3)

            # Inherit new a1 and a2 for top performers
            #top_performers_4 = [x[:] for x in best_params]
            #inheriteddampparams = object.InheritDampingParams(top_performers_4)
            #print("top performers 5: ", top_performers_4)


            # Generate 5 new random sets of parameters
            new_params = [0 for i in range(0,5)]
            for i in range(0,5):
                new_params[i] = object.SevenRandomNumbers()

            # combine all the new parameters to make generation i

            new_population = best_params + mutants + mutants_2 + mutants_3 + inherited

            for i in range(0,int(sys.argv[3])):
                Threads.append(i)
                
                T = "t" + str(i)
                # Store the command that runs each Cuby4 job
                command = object.MakeParamOptFile(new_population[i],i,Generation)
                # Store each command in a threaded subprocess.Popen command
                T = threading.Thread(target=call_script, args=(command,))
                Threads[i] = T



            for x in Threads:
                x.start()

            for x in Threads:
                x.join()
            del x
            



            for filename in sorted(os.listdir(current_path)):


                if filename.endswith(".out"):
                    associated_params = [0.0 for i in range(0,7)]
                    new_filename = current_path + "/" + filename
                    

                    command = ['grep', "Error:", new_filename]
                    grep = subprocess.Popen(command, stdout=subprocess.PIPE)
                    # output stores the final error from the optimization file
                    output = subprocess.check_output(('tail', '-1'), stdin=grep.stdout)
                    
                    if len(output) !=0:
                        output = output.split()[1]
                    else:
                        output = 100.0
                    
                    ERRORS.append(counter)
                    Files.append(counter)
                    Params.append(counter)
                    
                    ERRORS[counter] = output

                    Files[counter] = filename

                    

                    command2 = ['grep', "x0:", new_filename]
                    grep = subprocess.Popen(command2, stdout=subprocess.PIPE)
                    # output stores the final Cos parameter
                    output2 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                                      
                    if len(output2) !=0:
                        output2 = output2.split()[1]
                    else:
                        output2 = 0.0
                    
                    associated_params[0] = output2

                    command3 = ['grep', "x1:", new_filename]
                    grep = subprocess.Popen(command3, stdout=subprocess.PIPE)
                    # output stores the final Css parameter
                    output3 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    
                    if len(output3) !=0:
                        output3 = output3.split()[1]
                    else:
                        output3 = 0.0
                    
                    associated_params[1] = output3

                    command4 = ['grep', "d3_s8:", new_filename]
                    grep = subprocess.Popen(command4, stdout=subprocess.PIPE)
                    # output stores the final s8 parameter
                    output4 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    
                    if len(output4) !=0:
                        output4 = output4.split()[1]
                    else:
                        output4 = 0.0
                    
                    associated_params[2] = output4

                    command5 = ['grep', "d3_a1:", new_filename]
                    grep = subprocess.Popen(command5, stdout=subprocess.PIPE)
                    # output stores the final a1 parameter
                    output5 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    
                    if len(output5) !=0:
                        output5 = output5.split()[1]
                    else:
                        output5 = 0.0
                    
                    associated_params[3] = output5

                    command6 = ['grep', "d3_a2:", new_filename]
                    grep = subprocess.Popen(command6, stdout=subprocess.PIPE)
                    # output stores the final a2 parameter
                    output6 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    
                    if len(output6) !=0:
                        output6 = output6.split()[1]
                    else:
                        output6 = 0.0
                    
                    associated_params[4] = output6

                    command7 = ['grep', ":d3_double_damping_r", new_filename]
                    grep = subprocess.Popen(command7, stdout=subprocess.PIPE)
                    # output stores the final rcut parameter
                    output7 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    
                    if len(output7) !=0:
                        output7 = output7.split()[2]
                    else:
                        output7 = 0.0
                    
                    associated_params[5] = output7

                    command8 = ['grep', ":d3_double_damping_w", new_filename]
                    grep = subprocess.Popen(command8, stdout=subprocess.PIPE)
                    # output stores the final width
                    output8 = subprocess.check_output(('head', '-1'), stdin=grep.stdout)
                    
                    if len(output8) !=0:
                        output8 = output8.split()[2]
                    else:
                        output8 = 0.0
                    
                    associated_params[6] = output8
                    # Parameters for CKS Energy

                    Params[counter] = associated_params

                    counter += 1


        # zip and sort errors with associated parameter sets so the top performers are at the front
        ERRORS,Params = (list(t) for t in zip(*sorted(zip(ERRORS,Params))))

        # Contains the best five parameter sets from the initial population
        best_params = Params[:5]
        
        best_errors = ERRORS[:5]
        

        print("The most fit parameters are: ", best_params)
        print("the associated errros are: ", best_errors)



        All_Errors.append(f)
        All_Generations.append(f)
        All_Errors[f] = ERRORS
        All_Generations[f] = Generation

    # Can be implemented to store data for visualization of the optimization process
    #Data_File = open("Data_file.txt","a")
    #Data_File.write(str(All_Errors))
    #Data_File.write("\n")
    #Data_File.write(str(All_Generations))
    #Data_File.write("\n")
    #Data_File.close()






if __name__ == '__main__':
    main()
