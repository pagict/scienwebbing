import os
import sys

program_path = 'src/scienWebbing'
link_path = '/usr/sbin/scienWebbing'

if 'install' in sys.argv:
    python_path = sys.executable
    pgm = open(program_path, 'w')
    pgm.writelines('#!'+python_path+'\n')
    pre_pgm = open(program_path+'.py', 'r')
    pgm_content = pre_pgm.read()
    pgm.write(pgm_content)
    pgm.close()
    pre_pgm.close()

    try:
        os.chmod(program_path, 0510)
        os.symlink(os.path.join(os.getcwd(), program_path), link_path)
    except:
        print('Install failed. Please verify run with enough privileges')
    else:
        print('Install succeed!')
elif 'uninstall' in sys.argv:
    try:
        os.remove(link_path)
        os.remove(program_path)
    finally:
        print('Uninstall succeed!')