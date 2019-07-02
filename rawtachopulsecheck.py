import csv
import sys
from enum import Enum




class LogsParseState(Enum):
    FIND_BEGINNING = 1
    FIND_NEXT = 2



def perTacho_CalcDeltaPulseCount(newValue, oldValue):
    result = (0xffff + 1 + newValue - oldValue) % (0xfff + 1)
    return result

# Process each line, and retrieve the following  fields
def main():
    with open(sys.argv[1], mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        parseState = LogsParseState.FIND_BEGINNING
        # to read the following variables
        # cycle
        # tachometerData1.rawPulseCount[0]
        # tachometerData1.rawPulseCount[1]
        # tachometerData2.rawPulseCount[0]
        # tachometerData1.rawPulseCount[1]
        cycle = 0
        tachometerData1_rawPulseCount0 = 0
        tachometerData1_rawPulseCount1 = 0
        tachometerData2_rawPulseCount0 = 0
        tachometerData2_rawPulseCount1 = 0
        prev_cycle = 0
        prev_tachometerData1_rawPulseCount0 = 0
        prev_tachometerData1_rawPulseCount1 = 0s
        prev_tachometerData2_rawPulseCount0 = 0
        prev_tachometerData2_rawPulseCount1 = 0
        MAX_DIFF_TACHO_VALUES = 4
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
                continue

            cycle = int(row["cycle"], 10)
            tachometerData1_rawPulseCount0 = int(row["tachometerData1.rawPulseCount[0]"], 10)
            tachometerData1_rawPulseCount1 = int(row["tachometerData1.rawPulseCount[1]"], 10)
            tachometerData2_rawPulseCount0 = int(row["tachometerData2.rawPulseCount[0]"], 10)
            tachometerData2_rawPulseCount1 = int(row["tachometerData2.rawPulseCount[1]"], 10)

            if (LogsParseState.FIND_BEGINNING == parseState):
                prev_cycle = cycle
                prev_tachometerData1_rawPulseCount0 = tachometerData1_rawPulseCount0
                prev_tachometerData1_rawPulseCount1 = tachometerData1_rawPulseCount1
                prev_tachometerData2_rawPulseCount0 = tachometerData2_rawPulseCount0
                prev_tachometerData2_rawPulseCount1 = tachometerData2_rawPulseCount1
                parseState = LogsParseState.FIND_NEXT
            elif (LogsParseState.FIND_NEXT == parseState):
                if (cycle - prev_cycle > 1 ) or (cycle < prev_cycle):
                    #if there was a gap in cycle, or if cycle count reset , we set current read row as beginning
                    prev_cycle = cycle
                    prev_tachometerData1_rawPulseCount0 = tachometerData1_rawPulseCount0
                    prev_tachometerData1_rawPulseCount1 = tachometerData1_rawPulseCount1
                    prev_tachometerData2_rawPulseCount0 = tachometerData2_rawPulseCount0
                    prev_tachometerData2_rawPulseCount1 = tachometerData2_rawPulseCount1
                    parseState = LogsParseState.FIND_NEXT
                else:
                    #check tacho 1
                    deltapulsereplica1 = perTacho_CalcDeltaPulseCount(tachometerData1_rawPulseCount0,
                                                                      prev_tachometerData1_rawPulseCount0)
                    deltapulsereplica2

            line_count += 1

        print(f'Processed {line_count} lines.')    


main()

