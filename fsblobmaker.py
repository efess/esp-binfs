import os
import io
import struct

# - index -
# 56 bytes - path/file

# 4 bytes - pointer
# 4 bytes - length

class FsBlobMaker:
    LENGTH_PATH = 56
    LENGTH_OFFSET = 4
    LENGTH_BYTE_LENGTH = 4

    def __init__(self):
        pass

    def make_it(self, options):
        files = self.get_files(options['path'], options['max_size'])
        
        if len(files) == 0:
            return

        self.dump_to_blob(files, options['output'])

    def dump_to_blob(self, files, output_file):
        index_size = self.LENGTH_PATH + self.LENGTH_OFFSET + self.LENGTH_BYTE_LENGTH
        index_count = len(files)

        index_offset = 4
        data_offset = index_offset + index_size * index_count
        try:
            with open(output_file, 'wb') as ofile:
                ofile.seek(0)
                ofile.write(struct.pack("<I", len(files)))
                
                for infile in files:
                    ofile.seek(index_offset)
                    ofile.write(bytes(infile['bin_path'], 'UTF-8'))
                    ofile.seek(index_offset + self.LENGTH_PATH)
                    ofile.write(struct.pack("<I", data_offset))
                    ofile.write(struct.pack("<I", infile['size']))
                    ofile.seek(data_offset)
                    try:
                        with open(infile['file_path'], 'rb') as ifile:
                            self.copy_data(ofile, ifile, infile['size'])
                    except IOError:
                        print('cannot open ' + infile['file_path'] + ' for reading')
                        return

                    data_offset += infile['size']
                    index_offset += index_size
                    
        except IOError:
            print('cannot open ' + output_file + ' for writing')
            return
        
        print('Wrote ' + str(data_offset) + ' bytes to ' + output_file)
    
    def copy_data(self, f_dest, f_src, size):
        buffer_size = 4096
        to_write = size

        while to_write > 0:
            this_write = min(to_write, buffer_size)
            f_dest.write(f_src.read(buffer_size))
            to_write -= this_write

    def get_files(self, root, max_size):
        index_size = self.LENGTH_PATH + self.LENGTH_OFFSET + self.LENGTH_BYTE_LENGTH
        total_size = 0
        files = []
        
        for dirname, dirnames, filenames in os.walk(root):

            # print path to all filenames.
            for filename in filenames:
                
                file_path = os.path.join(dirname, filename)                
                file_size = os.stat(file_path).st_size

                if total_size > max_size:
                    print("Directory size exceeds maximum at " + str(total_size))
                    return []

                bin_path = file_path.replace(root, '').replace('\\', '/')
                
                if (len(bin_path) - 1) > self.LENGTH_PATH: # -1 to account for terminating char
                    print("Path too long " + bin_path)
                    return []

                total_size += file_size
                total_size += index_size

                obj = {
                    'file_path': file_path,
                    'bin_path': file_path.replace(root, '').replace('\\', '/'),
                    'size': file_size
                }

                files.append(obj)


        #for obj in files:
        #    print obj['bin_path'] + "  " + str(obj['size'])
        

        #print total_size

        return files