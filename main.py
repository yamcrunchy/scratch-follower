import scratchattach as scratch3

id = "1059331686"
session_id = open('info.txt', 'r').read() #put your session id here
session = scratch3.Session(session_id, username="dyptfolt314")
conn = session.connect_cloud(id)
events = scratch3.CloudEvents(id)
encoding = "abcdefghijklmnopqrstuvwxyz1234567890-_"
decode_dict = {f"{i:02d}": char for i, char in enumerate(encoding, start=1)}
stored_username = scratch3.get_var(id, "username")
stored_operational_response = scratch3.get_var(id, "change")

if __name__ == "__main__":
    print(scratch3.get_var(id, "username"))
    print(scratch3.get_var(id, "change"))
    print(session_id)
    events.start(thread=True)

def decode(val):
    if val is not None:
        decoded_str = "" 
        for i in range(0, len(val), 2):
            code = val[i:i+2]
            decoded_str += decode_dict.get(code, "?")
        return decoded_str
    else:
        return None

def on_ready():
   print("Event listener ready!")

@events.event
def on_set(event):
    global stored_username
    if scratch3.get_var(id, "operational_response") != scratch3.get_var(id, "change") and event.var != "operational_response":
        conn.set_var("operational_response", scratch3.get_var(id, "change"))
        print("Operational Status Updated")
    if stored_username == scratch3.get_var(id, "username"):
        pass
    elif stored_username != scratch3.get_var(id, "username"):
        username = decode(scratch3.get_var(id, "username"))
        print(username)
        user = session.connect_user(username)
        user.follow()
        print("followed " + username)
        stored_username = scratch3.get_var(id, "username")
        f = open('users.txt', 'a')
        f.write(username + '\n')
        f.close()
