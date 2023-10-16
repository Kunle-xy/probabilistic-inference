from utils import helper
import utils
import main
import subprocess

result= subprocess.run(['python', 'main.py', '--line_1', '810,350,990,270', \
                    "--line_2", '810,295,990,290', "--weight_1", "0.5", "--weight_2", "0.5", "--section", "0.3", "--shift_rate", "10"],capture_output=True, text=True) \

print(result.stdout.split(',')[0], result.stdout.split(',')[1], result.stdout.split(',')[2])



