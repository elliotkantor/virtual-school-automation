#! python3
# main.py - interactively controls virtual school
import pandas as pd
import zoomAutomation
import scrapeSchoology
time_df = pd.read_csv('timings.csv')



while True:
    # checks if weekend
    if not isWeekday() and not continueOnWeekend:
        choice = input("It is a weekend. Continue anyway? (y/n) ").strip().lower()
        if not choice.startswith('y'):
            print("Ending program...\n")
            break
        else:
            continueOnWeekend = True
            print("Continuing...\n")
            # implied continue

    # check if current time in csv
    now = datetime.now().strftime("%H:%M")
    if now in str(df['timings']):
        # find the proper row index with the right time
        current_row_index = time_df.loc[time_df['timings'] == now].index.values.astype('int')[0]
        current_type = time_df.loc[current_row_index, 'type']

        if current_type == 'zoom':
            zoomID =
            zoomPass =
            zoomAutomation.sign_in(zoomID, zoomPass)
            print("Signed in to " + time_df.loc[current_row_index, 'classname'])
        elif current_type == 'schoology':
            pass
        elif current_type == 'zoomEmbed':
            pass
        else:
            print(f"Did not recognize {current_type} as a type.")


    time.sleep(15)
