# Getter get-username
hello = Hello { $username }!
# Start message text
firstrow = This is a blood pressure diary.
secondrow = It will help track your blood pressure, pulse and well-being.
thirdrow = Doctors recommend filling out such diaries every day.
fourthrow = The doctor will receive more reliable information about
fifthrow = your health and will be able to note at what time you are at risk
sixthrow = and when it is best for you to take the necessary medications.
seventhrow = A little about how to keep a diary.
eighthrow = It is better to measure blood pressure in the morning, at lunchtime and in the evening.
ninthrow = It is advisable to indicate your general health and what medications were taken.
tenthrow = If the bot suddenly breaks or you want to contact me, write
eleventhrow = In order to receive the diary by email, you must enter your email address.
twelfthrow = Necessary formality: by sending your email address, you agree to the processing
thirteenthrow = of data
fourteenthrow = Use my bots:
fiveteenthrow = Bot for checking drugs for proven effectiveness.
sixteenthrow = Reference book on medicines.
seventeenthrow = Handbook of medicinal plants.
eighteenthrow = You can control the bot using buttons 👇
entry = Record measured data in a diary
missed = Record data in a diary for the past date
timezone = Change time zone
entries-display = Display the last 20 entries
geting-diary = Get the diary as a table Exel
statistics = Show the last 45 records as a graph
deletion-diary = Delete the diary with all entries
enter-email = Enter or replace email to send the diary
diary-send = Send your diary as a table by email
doctor-send = Send the diary to your doctor by email

# Getter get-user-id
quest-deletion = Are you sure you want to delete all your entries?
deletion = Delete
cancel-deletion = Cancel deletion

# Getter result-getter
change-systolic = Change systolic pressure
change-diastolic = Change diastolic pressure
change-pulse = Change heart rate
change-arrhythmia = Change the presence of arrhythmia
change-comment = Edit comment
save-data = Save data
you-entered = You entered
systolic-press = Systolic pressure
diastolic-press = Diastolic pressure
pulse = Pulse
arrhythmia = Arrhythmia
comment = A comment
entry-cancel = Cancel data entry
edit-cancel = Cancel data change

# Getter get-email
but-cancel = Cancel
sending = Send
sending_diary = To send the diary to the { $email }, click the "Send" button
press-cancel = To cancel, click "Cancel"
save-email = To save your email, click the "Save" button.
press-save = Save

# Getter get-user-email
question_send = Send your diary to: { $email }?
change_email = Change email
no_email = To send a diary, you must first enter your email.
next_start = To continue working with the bot, click the "Start" button
start = Start

# Getter get-number-rows-userdata
no_data = First you need to make at least one entry in your diary.
but_next = Next
next_del_data = To delete all your entries, click "Next"
next_send_email = To send the diary by email, click "Next"
show_or_cancel_graph = To show the graph, click "Show graph"
three_diary_entries = To build a graph, you need at least three diary entries.
show_graph = Show graph
next_table = To get the diary in table form, click "Next"
receive_diary = To receive the diary, click "Get diary"
get_table = Get diary
next_display_entry = To display the last 20 entries, click "Next"

# Getter get-timezone
utc1 = UTC+1 - London
utc2 = UTC+2 - Kaliningrad
utc3 = UTC+3 - Moscow
utc4 = UTC+4 - Samara
utc5 = UTC+5 - Ekaterinburg
utc6 = UTC+6 - Omsk
utc7 = UTC+7 - Tomsk
utc8 = UTC+8 - Irkutsk
utc9 = UTC+9 - Yakutsk
utc10 = UTC+10 - Vladivostok
utc11 = UTC+11 - Magadan
utc12 = UTC+12 - Petropavlovsk-Kamchatsky
select_timezone = Select your time zone so that the time in your diary is displayed correctly.
save_timezone = To save your time zone, click the "Save" button.

# Getter get-texts-finished
confirm_delete = All your entries have been deleted.
send_diary = The diary has been sent!
save_email = Email saved!
save_result = Data saved!
update_save = Data has been updated and saved.
saving_timezone = Time zone saved!

# Getter get-texts-input-email
input_email = Enter your email to which your diary will be sent

# Getter get-texts-entry-dialog
edit_cancel = Undo editing
date_selection = Select the date when the measurements were taken
time_selection = Select the hour when the measurements were taken
entry_systolic = Enter your upper (systolic) pressure
entry_diastolic = Enter your lower (diastolic) pressure
entry_pulse = Enter your heart rate.
entry_zero = If you did not measure your pulse, enter zero.
presence_arrhythmia = Check if you currently have arrhythmia
write_comment = Write a comment in the message about how you are feeling and what medications you took
press_save = Click the "Save" button to save the entered data
word_yes = Yes
word_no = No
unknown = Unknown

# Getter get-data
delete_edit_row = Should I delete or edit the entry with the date { $result }?
delete_row = Delete entry with date { $result }
edit_row = Edit an entry with the date { $result }
mark_row = Mark the entry you want to edit or delete 👇

# Getter get-row
word_was = Was:

# Getter get-texts-dialogs
row_delete = Post deleted

# email-dialog handler incorrect-email
incorrect_input = Invalid input. Try again.
cancel_input = If you want to cancel your entry, click "Cancel"

# entry-dialog handler incorrect-comment
long_comment = Comment too long. Reduce the number of characters to 50.

# send_dialog handler send-email
text_email = Hello! This is CardioBot. There is no need to respond to this letter. The blood pressure diary is attached to this letter.

# other-handler
service_mode = The bot is in maintenance mode. Please wait.

# MiddlewareBanned
you_banned = You are banned from the bot!
