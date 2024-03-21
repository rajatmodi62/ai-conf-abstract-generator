from txt2pdf import generate_pdf
import glob 


# root = '/Users/rajat/personal/proceeding_generator/nips/txt/nips_2023.txt'
# root = '/Users/rajat/personal/proceeding_generator/nips/txt/**/*.txt'
txts = glob.glob('*.txt')
# txts = ['/home/rmodi/ssd/ai-conf-abstract-generator/iccv23.txt']
for txt in txts:
    generate_pdf(txt)