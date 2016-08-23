#!/usr/bin/env python

'''
:mod:`sar.multiparser` is a module containing class for parsing SAR output
files where multiple files are merged into one huge file.

.. WARNING::
   Parses SAR ASCII output only, not binary files!

.. WARNING::
   Parses SAR ASCII files only, **not** ``SAR -A`` output! \
   (24hr output compared to AM/PM output).
   Following versions might support ``SAR -A`` parsing.

'''

import sar.parser as sarparse
from sar import PATTERN_MULTISPLIT
import mmap
import os
import traceback
from types import StringType


class Multiparser(object):
    '''
    Multifile parser for SAR files. Derives from SAR Parser class
        :param filename: Name of the SAR output file, with combined data
        :type filename: str.
    '''

    def __init__(self, combo_filename=''):

        self.__sarinfos = {}
        '''Dictionary for multiple dictionaries from
           :class:`com.nimium.sys.util.sar.parser.Parser`'''
        self.__splitpointers = []
        '''List of pointers inside combo file where each file starts'''
        self.__filename = combo_filename
        '''SAR output filename to be parsed'''

        return None

    def load_file(self):
        '''
        Loads combined SAR format logfile in ASCII format.
            :return: ``True`` if loading and parsing of file went fine, \
            ``False`` if it failed (at any point)
        '''
        daychunks = self.__split_file()

        if (daychunks):

            maxcount = len(self.__splitpointers)
            for i in range(maxcount):
                start = self.__splitpointers[i]
                end = None
                if (i < (maxcount - 1)):
                    end = self.__splitpointers[i + 1]

                chunk = self.__get_chunk(start, end)

                parser = sarparse.Parser()
                cpu_usage, mem_usage, swp_usage, io_usage = \
                    parser._parse_file(parser._split_file(chunk))

                self.__sarinfos[self.__get_part_date(chunk)] = {
                    "cpu": cpu_usage,
                    "mem": mem_usage,
                    "swap": swp_usage,
                    "io": io_usage
                }
                del(cpu_usage)
                del(mem_usage)
                del(swp_usage)
                del(io_usage)
                del(parser)

            return(True)

    def get_sar_info(self):
        '''
        Returns parsed sar info
            :return: ``Dictionary``-style list of SAR data
        '''
        return self.__sarinfos

    def __get_chunk(self, start=0, end=None):
        '''
        Gets chunk from the sar combo file, from start to end
            :param start: where to start a pulled chunk
            :type start: int.
            :param end: where to end a pulled chunk
            :type end: int.
            :return: str.
        '''
        piece = False

        if (self.__filename and os.access(self.__filename, os.R_OK)):

            fhandle = None

            try:
                fhandle = os.open(self.__filename, os.O_RDONLY)
            except OSError:
                print(("Couldn't open file %s" % (self.__filename)))
                fhandle = None

            if (fhandle):

                try:
                    sarmap = mmap.mmap(fhandle, length=0, prot=mmap.PROT_READ)
                except (TypeError, IndexError):
                    os.close(fhandle)
                    traceback.print_exc()
                    #sys.exit(-1)
                    return False

                if (not end):
                    end = sarmap.size()

                try:
                    sarmap.seek(start)
                    piece = sarmap.read(end - start)
                except:
                    traceback.print_exc()

            os.close(fhandle)

        return(piece)

    def __split_file(self):
        '''
        Splits combined SAR output file (in ASCII format) in order to
        extract info we need for it, in the format we want.
            :return: ``List``-style of SAR file sections separated by
                the type of info they contain (SAR file sections) without
                parsing what is exactly what at this point
        '''
        # Filename passed checks through __init__
        if (self.__filename and os.access(self.__filename, os.R_OK)):

            fhandle = None

            try:
                fhandle = os.open(self.__filename, os.O_RDONLY)
            except OSError:
                print(("Couldn't open file %s" % (self.__filename)))
                fhandle = None

            if (fhandle):

                try:
                    sarmap = mmap.mmap(fhandle, length=0, prot=mmap.PROT_READ)
                except (TypeError, IndexError):
                    os.close(fhandle)
                    traceback.print_exc()
                    #sys.exit(-1)
                    return False

            sfpos = sarmap.find(PATTERN_MULTISPLIT, 0)

            while (sfpos > -1):

                '''Split by day found'''
                self.__splitpointers.append(sfpos)

                # Iterate for new position
                try:
                    sfpos = sarmap.find(PATTERN_MULTISPLIT, (sfpos + 1))
                except ValueError:
                    print("ValueError on mmap.find()")
                    return True

            if (self.__splitpointers):
                # Not sure if this will work - if empty set
                # goes back as True here
                return True

        return False

    def __get_part_date(self, part=''):
        '''
        Retrieves date of the combo part from the file
            :param part: Part of the combo file (parsed out whole SAR file
                from the combo
            :type part: str.
            :return: string containing date in ISO format (YYY-MM-DD)
        '''
        if (type(part) is not StringType):
            # We can cope with strings only
            return False

        firstline = part.split("\n")[0]

        info = firstline.split()
        datevalue = ''

        try:
            datevalue = info[3]

        except KeyError:
            datevalue = False

        except:
            traceback.print_exc()
            datevalue = False

        return(datevalue)
