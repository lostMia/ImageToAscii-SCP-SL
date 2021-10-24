from PIL import Image
import argparse


##########################################################################################################################################################################################################################
#                                                                                                                                                                                                                        #
#   Script by lostMia [Discord: lostMia#0430]                                                                                                                                                                            #
#                                                                                                                                                                                                                        #
#   Takes any Image [Supportet by Pillow 8.4.0 (https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#image-file-formats)] and converts it to a String consisting of ASCII Characters and HTML Tags.  #
#   These, when pasted into the SCP:SL Console, will display given image in textform [Max: 53 x 244 Chrs] in grayscale. Trying to compress more will cause the image to go over the limit of ~15k Chrs and not show up.  #
#   Should display correctly on 1080p and 4k                                                                                                                                                                             #
#                                                                                                                                                                                                                        #
##########################################################################################################################################################################################################################



def create_outputfile():
    try:
        # create outputfile if it doesnt exist and clear any contents
        outfile = open('output.txt', 'w')
        outfile.close()

        print("- Created output.txt         | \u221A |")

    except:

        print("- Created output.txt         | X |")
        print("\n=============================================================================================================\n")

        raise 


def get_image_data(rows1, imgname1):
    try:
        # open file and load data
        img = Image.open(imgname1)
        width, height = img.size
        ratio = width / height

        # set rows to 53, if above that
        if rows1 > 53:
            rows1 = 53
            print("---The row value was reset back to 53---")

        # calculate the lines needed
        lines1 = int((rows1 * ratio) * 2)

        # checks if row length exceeds the consoles limits (244)
        if lines1 > 244:
            # ratio, that the rows must be scaled down to, in order to fit the whole image
            scaledownratio = lines1 / 244
            rows1 = int(rows1 / scaledownratio)# -1 just to be safe

            # calculate the lines needed
            lines1 = int((rows1 * ratio) * 2)
        
        # resize to lines and rows needed
        img = img.resize((lines1, rows1)).convert('L')
        imgdata1 = img.load()

        print("- Loaded the Image           | \u221A |")

        return rows1, lines1, imgdata1

    except:

        print("- Failed to load Image       | X |")
        print("\n=============================================================================================================\n")
        
        raise 


def write_to_output(rows2, lines2, imgdata2, grayscale2):
    try:
        # open output file in append mode
        outfile = open('output.txt', 'a', encoding=('utf-8'))

        # adds opening HTML tags at the start of the file
        outfile.write('<color="white"><size=8>')

        # for every pixel in the image
        for y in range(0, rows2):
            for x in range(0, lines2):

                # get light value
                total_rgb_value = imgdata2[x, y] # 0 - 255

                # get ascii character acording to light value
                asciichr = grayscale2[int((total_rgb_value * 9) / 255)] # 0 - 69

                # write ascii character to output file
                outfile.write(asciichr)

            # adds unicode spaces to fill the rest of the line
            rem_space = 243 - x
            #outfile.write('\u2004' * rem_space)
            outfile.write('\n')

        # adds closing HTML tags at the end of the file
        outfile.write('.</size></color>')
        outfile.close()

        print("- Converted to ASCII         | \u221A |")

    except:

        print("- Failed conversion to ASCII | X |")
        print("\n=============================================================================================================\n")

        raise 


def main():
    # create parser
    parser = argparse.ArgumentParser()

    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=False)
    parser.add_argument('--rows', dest='rows', required=False)
    parser.add_argument('--inv', dest='inv', required=False)

    # parse down args
    args = parser.parse_args()

    # override default value if argument was given
    rows = 53
    if args.rows:
        rows = int(args.rows)

    # override default value if argument was given
    imagename = '[NO IMAGE SELECTED]'
    if args.imgFile:
        imagename = args.imgFile

    # Inverts grayscale, if the invert parameter is parsed
    grayscale = " .:-=+*#%@"
    if args.inv:
        grayscale = "@%#*+=-:. "


    # creates the output file if missing and clears the contents
    create_outputfile()

    # gets image data and calculates the number of lines needet
    rows, lines, imgdata = get_image_data(rows, imagename)

    # converts image to ASCII and writes it to output.txt
    write_to_output(rows, lines, imgdata, grayscale)

if __name__ == '__main__':
    main()