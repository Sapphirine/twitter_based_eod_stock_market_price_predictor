#!/usr/bin/env python
import csv

def pivotCSVFile( fileName ):
    ''' This function takes in a filename, reads the file, adds the dates as keys to a dictionary so
        that they are unique, and aggregates all texts that correspond to that date into one resulting value
    '''
    # Temp dictionary to store values
    finalData = []
    pivotData = {}
    # Open the file and read the contents
    # Add texts for same dates to a list
    with open( fileName ) as inFile:
        readr = csv.reader( inFile )
        for row in readr:
            text = row[ 0 ]
            date = row[ 1 ]
            if date in pivotData:
                pivotData[ date ].append( text )
            else:
                pivotData[ date ] = [ text ]
    inFile.close()
    # Convert the list of values to comma seperated string
    for k,v in pivotData.iteritems():
        strValues = ",".join( v )
        pivotData[ k ] = strValues
    # Create a temp dict corresponding to each row
    # Write back the dictionary as a csv
    with open( fileName[:-4 ]+'_pivot.csv', 'a+' ) as outFile:
        tempDict = {}
        fieldNames = [ 'date', 'text' ]
        w = csv.DictWriter( outFile, fieldNames )
        for k,v in pivotData.iteritems():
            tempDict[ fieldNames[ 0 ] ] = k
            tempDict[ fieldNames[ 1 ]  ] = v
            w.writerow( tempDict )
    outFile.close()

if __name__ == "__main__":
    import sys
    pivotCSVFile( sys.argv[ 1 ] )


