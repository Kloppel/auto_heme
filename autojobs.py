import sys 
import os 
import subprocess as proc 
import textwrap
import inspect

class automation():
    def __init__(self):
        """ 
        Class that creates the necessary files for running jobs automatically except for the .xyz coordinate files. 
        """

    def __create_runtime_folders(pdb_list, spin_states):
        for pdb_id in pdb_list:
            for spin_state in spin_states:
                if not os.path.exists(f"{pdb_id}"):
                    os.mkdir(f"{pdb_id}")
                if not os.path.exists(f"{pdb_id}/{pdb_id}_{spin_state}/"):
                    os.mkdir(f"{pdb_id}/{pdb_id}_{spin_state}/")
        return

    def __create_gaussian_scripts_01(pdb_id):
        link0=f"""%nprocs=12
        %mem=16GB
        %chk={pdb_id}_II_S.chk
        # polar def2tzvp empiricaldispersion=gd3bj pbe1pbe

        {pdb_id}_II_S 

        0 1
        """

        link1=f"""

        --Link1--
        %nprocs=12
        %mem=16GB
        %chk={pdb_id}_II_S.chk
        # PBE1PBE/def2TZVP empiricaldispersion=GD3BJ int=(grid=ultrafine) geom=check guess=read pop=nbo scf=qc

        {pdb_id}_II_S_nbo

        0 1
        """

        link2=f""" 
        --Link2--
        %nprocs=12
        %mem=16GB
        %chk={pdb_id}_II_S.chk
        # PBE1PBE/def2TZVP empiricaldispersion=GD3BJ int=(grid=ultrafine) geom=check guess=read scrf=(smd,solvent=Chloroform) 

        {pdb_id}_II_S_solv 

        0 1 

        """
        coords=open(f"pdb_coord/{pdb_id}.xyz").read()
        com01=inspect.cleandoc(link0)+"\n"+coords+inspect.cleandoc(link1)+inspect.cleandoc(link2)
        com=open(f"{pdb_id}/{pdb_id}_01/{pdb_id}01.com", "w").write(com01)
        return

    def __create_gaussian_scripts_05(pdb_id):
        link3=f"""--Link3--
        %nprocs=12
        %mem=16GB
        %oldchk={pdb_id}_II_S.chk
        %chk={pdb_id}_II_Q.chk
        # PBE1PBE/def2TZVP empiricaldispersion=GD3BJ scf=maxcycle=999 geom=check pop=nbo

        {pdb_id}_II_Q

        0 5

        """

        link4=f"""--Link4--
        %nprocs=12
        %mem=16GB
        %chk={pdb_id}_II_Q.chk
        # PBE1PBE/def2TZVP empiricaldispersion=GD3BJ geom=check guess=read scrf=(smd,solvent=Chloroform)

        {pdb_id}_II_Q_solv

        0 5

        """

        com05=inspect.cleandoc(link3)+inspect.cleandoc(link4)
        com=open(f"{pdb_id}/{pdb_id}_05/{pdb_id}05.com", "w").write(com05)
        return

    def __create_gaussian_scripts_12(pdb_id):
        link5=f"""--Link5--
        %nprocs=12
        %mem=16GB
        %oldchk={pdb_id}_II_S.chk
        %chk={pdb_id}_III_D.chk
        # PBE1PBE/def2TZVP empiricaldispersion=GD3BJ scf=maxcycle=999 geom=check pop=nbo

        {pdb_id}_III_D

        1 2

        """

        link6=f"""--Link6--
        %nprocs=12
        %mem=16GB
        %chk={pdb_id}_III_D.chk
        # PBE1PBE/def2TZVP empiricaldispersion=GD3BJ geom=check guess=read scrf=(smd,solvent=Chloroform)

        {pdb_id}_III_D_solv

        1 2

        """

        com12=inspect.cleandoc(link5)+inspect.cleandoc(link6)
        com=open(f"{pdb_id}/{pdb_id}_12/{pdb_id}12.com", "w").write(com12)
        return
    
    def __create_gaussian_scripts_16(pdb_id):
        link7=f"""--Link7--
        %nprocs=12
        %mem=16GB
        %oldchk={pdb_id}_III_D.chk
        %chk={pdb_id}_III_H.chk
        # PBE1PBE/def2TZVP empiricaldispersion=GD3BJ scf=maxcycle=999 geom=check pop=nbo

        {pdb_id}_III_H

        1 6

        """

        link8=f"""--Link8--
        %nprocs=12
        %mem=16GB
        %chk={pdb_id}_III_H.chk
        # PBE1PBE/def2TZVP empiricaldispersion=GD3BJ geom=check guess=read scrf=(smd,solvent=Chloroform)

        {pdb_id}_III_H_solv

        1 6

        """

        com16=inspect.cleandoc(link7)+inspect.cleandoc(link8)
        com=open(f"{pdb_id}/{pdb_id}_16/{pdb_id}16.com", "w").write(com16)
        return
    
    def __create_rerun_gaussian_scripts_05(pdb_id):
        link3re = f""" --Link3--
        %nprocs=12
        %mem=16GB
        %oldchk={pdb_id}_II_S.chk
        %chk={pdb_id}_II_Sre.chk
        # PBE1PBE/gen scf=maxcycle=999 geom=check

        {pdb_id}_II_Q

        0 5

        C N O H 0
        6-31G*
        ****
        Fe 0
        TZVP
        ****


        """ 
        com05re=inspect.cleandoc(link3re)
        if not os.path.exists(f"{pdb_id}/{pdb_id}_05re/"):
            os.mkdir(f"{pdb_id}/{pdb_id}_05re/")
        com=open(f"{pdb_id}/{pdb_id}_05re/{pdb_id}05re.com", "w").write(com05re)
        return
    
    def __create_rerun_gaussian_scripts_12(pdb_id):
        link5re = f""" --Link5--
        %nprocs=12
        %mem=16GB
        %oldchk={pdb_id}_II_S.chk
        %chk={pdb_id}_II_Sre.chk
        # PBE1PBE/gen scf=maxcycle=999 geom=check

        {pdb_id}_III_D

        1 2

        C N O H 0
        6-31G*
        ****
        Fe 0
        TZVP
        ****


        """ 
        com12re=inspect.cleandoc(link5re)
        if not os.path.exists(f"{pdb_id}/{pdb_id}_12re/"):
            os.mkdir(f"{pdb_id}/{pdb_id}_12re/")
        com=open(f"{pdb_id}/{pdb_id}_12re/{pdb_id}12re.com", "w").write(com12re)
        return

    def __create_rerun_gaussian_scripts_16(pdb_id):
        link7re = f""" --Link7--
        %nprocs=12
        %mem=16GB
        %oldchk={pdb_id}_III_D.chk
        %chk={pdb_id}_III_Dre.chk
        # PBE1PBE/gen scf=maxcycle=999 geom=check

        {pdb_id}_III_H

        1 6

        C N O H 0
        6-31G*
        ****
        Fe 0
        TZVP
        ****


        """ 
        com16re=inspect.cleandoc(link7re)
        if not os.path.exists(f"{pdb_id}/{pdb_id}_16re/"):
            os.mkdir(f"{pdb_id}/{pdb_id}_16re/")
        com=open(f"{pdb_id}/{pdb_id}_16re/{pdb_id}16re.com", "w").write(com16re)
        return

    def __write_jobscript(pdb_id, spin_state, jobtext):
        if not os.path.exists(f"{pdb_id}/{pdb_id}_{spin_state}/"):
            os.mkdir(f"{pdb_id}/{pdb_id}_{spin_state}/")
        bash=open(f"{pdb_id}/{pdb_id}_{spin_state}/{pdb_id}{spin_state}.job", "w").write(jobtext)
        return

    def __create_jobscript(pdb_id, spin_state):
        jobtext=f"""#!/bin/bash --login
        #$ -cwd
        #$ -pe mp 4
        #$ -N {pdb_id}_{spin_state}
        #$ -o gaussian.out
        #$ -j y
        #$ -l h_rt=604800
        #$ -m ea
        #$ -M elizaveta.zhartovska@campus.tu-berlin.de  

        module load g16
        #declare -x GAUSS_SCRDIR="${{SCRATCHDIR}}"

        STOREDIR=$1
        COMNAME=$2

        if [ ! -s ${{STOREDIR}}/${{COMNAME}} ]; then
        echo "Error: input file ${{STOREDIR}}/${{COMNAME}} does not exist!"
        exit 1
        fi

        SCRATCHDIR=$(mktemp -d /scratch/zhartovska_gaussian.XXXXXXX)
        chmod go+rwx ${{SCRATCHDIR}}
        cd ${{SCRATCHDIR}}
        cp ${{STOREDIR}}/*.chk ${{SCRATCHDIR}}/
        cp ${{STOREDIR}}/*.com ${{SCRATCHDIR}}/

        g16 ${{STOREDIR}}/${{COMNAME}}
        sleep 5

        mv -f ${{SCRATCHDIR}}/*.chk ${{STOREDIR}}/
    
        ### cp -a ${{SCRATCHDIR}}  ${{STOREDIR}}/${{COMNAME}}_scratch

        ls -al ${{SCRATCHDIR}}

        cd ${{STOREDIR}}
        #formchk *.chk
        rm -r ${{SCRATCHDIR}}

        echo "        " >> /net/work/zhartovska/BioModel/timeofqg.txt
        echo $PWD $1 >> /net/work/zhartovska/BioModel/timeofqg.txt
        timedatectl|grep Local >> /net/work/zhartovska/BioModel/timeofqg.txt
        echo "       " >> /net/work/zhartovska/BioModel/timeofqg.txt
        echo ____ >> /net/work/zhartovska/BioModel/timeofqg.txt
        """
        jobtext=inspect.cleandoc(jobtext)
        automation.__write_jobscript(pdb_id=pdb_id, spin_state=spin_state, jobtext=jobtext)
        return
    
    def __write_jobscript_re(pdb_id, spin_state, jobtext):
        if not os.path.exists(f"{pdb_id}/{pdb_id}_{spin_state}re/"):
            os.mkdir(f"{pdb_id}/{pdb_id}_{spin_state}re/")
        bash=open(f"{pdb_id}/{pdb_id}_{spin_state}re/{pdb_id}{spin_state}re.job", "w").write(jobtext)
        return

    def __create_jobscript_re(pdb_id, spin_state):
        jobtext=f"""#!/bin/bash --login
        #$ -cwd
        #$ -pe mp 4
        #$ -N {pdb_id}_{spin_state}
        #$ -o gaussian.out
        #$ -j y
        #$ -l h_rt=604800
        #$ -m ea
        #$ -M elizaveta.zhartovska@campus.tu-berlin.de  

        module load g16
        #declare -x GAUSS_SCRDIR="${{SCRATCHDIR}}"

        STOREDIR=$1
        COMNAME=$2

        if [ ! -s ${{STOREDIR}}/${{COMNAME}} ]; then
        echo "Error: input file ${{STOREDIR}}/${{COMNAME}} does not exist!"
        exit 1
        fi

        SCRATCHDIR=$(mktemp -d /scratch/zhartovska_gaussian.XXXXXXX)
        chmod go+rwx ${{SCRATCHDIR}}
        cd ${{SCRATCHDIR}}
        cp ${{STOREDIR}}/*.chk ${{SCRATCHDIR}}/
        cp ${{STOREDIR}}/*.com ${{SCRATCHDIR}}/

        g16 ${{STOREDIR}}/${{COMNAME}}
        sleep 5

        mv -f ${{SCRATCHDIR}}/*.chk ${{STOREDIR}}/

        ### cp -a ${{SCRATCHDIR}}  ${{STOREDIR}}/${{COMNAME}}_scratch

        ls -al ${{SCRATCHDIR}}

        cd ${{STOREDIR}}
        #formchk *.chk
        rm -r ${{SCRATCHDIR}}

        echo "        " >> /net/work/zhartovska/BioModel/timeofqg.txt
        echo $PWD $1 >> /net/work/zhartovska/BioModel/timeofqg.txt
        timedatectl|grep Local >> /net/work/zhartovska/BioModel/timeofqg.txt
        echo "       " >> /net/work/zhartovska/BioModel/timeofqg.txt
        echo ____ >> /net/work/zhartovska/BioModel/timeofqg.txt
        """ 
        jobtext=inspect.cleandoc(jobtext)
        automation.__write_jobscript_re(pdb_id=pdb_id, spin_state=spin_state, jobtext=jobtext)
        return

    def __create_gaussian_scripts_all(pdb_ids):
        for pdb_id in pdb_ids:
            automation.__create_gaussian_scripts_01(pdb_id=pdb_id)
            automation.__create_gaussian_scripts_05(pdb_id=pdb_id)
            automation.__create_gaussian_scripts_12(pdb_id=pdb_id)
            automation.__create_gaussian_scripts_16(pdb_id=pdb_id)
            automation.__create_rerun_gaussian_scripts_05(pdb_id=pdb_id)
            automation.__create_rerun_gaussian_scripts_12(pdb_id=pdb_id)
            automation.__create_rerun_gaussian_scripts_16(pdb_id=pdb_id)
        return

    def __create_jobscripts_all(pdb_ids, spin_states):
        for pdb_id in pdb_ids:
            for spin_state in spin_states:
                automation.__create_jobscript(pdb_id=pdb_id, spin_state=spin_state)
        for pdb_id in pdb_ids:
            for spin_state in spin_states[1:]:
                automation.__create_jobscript_re(pdb_id=pdb_id, spin_state=spin_state)
        return
        
    def main():
        spin_states=["01", "05", "12", "16"]
        pdb_list=["3hb3", "2gsm"]
        automation.__create_runtime_folders(pdb_list=pdb_list, spin_states=spin_states)
        automation.__create_gaussian_scripts_all(pdb_ids=pdb_list)
        automation.__create_jobscripts_all(pdb_ids=pdb_list, spin_states=spin_states)
        return

