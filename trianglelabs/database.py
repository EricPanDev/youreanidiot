import time
import os
class database:
    def create_if_nonexistant(struct: list, default_value=""):
        file = struct[-1]
        struct = struct[:-1]
        added = ""
        for i in range(len(struct)):
            added += struct[i] + "/"
            if not os.path.exists(added):
                os.mkdir(added)
        if not os.path.exists(added + file):
            with open(added + file, "w") as file_creation:
                file_creation.write(default_value)
                file_creation.close()

    def set_message_limit(id, limit):
        id = str(id)
        file = ["database", "limits", id, "messages", "max"]
        database.create_if_nonexistant(file, "50")
        with open('/'.join(file), "w") as limit_file:
            limit_file.write(str(limit))
            limit_file.close()

    def set_art_limit(id, limit):
        id = str(id)
        file = ["database", "limits", id, "art", "max"]
        database.create_if_nonexistant(file, "5")
        with open('/'.join(file), "w") as limit_file:
            limit_file.write(str(limit))
            limit_file.close()

    def get_limits(id):
        id = str(id)
        file1 = ["database", "limits", id, "messages", "max"]
        file2 = ["database", "limits", id, "art", "max"]
        file3 = ["database", "limits", id, "backstory", "max"]
        database.create_if_nonexistant(file1, "50")
        database.create_if_nonexistant(file2, "5")
        database.create_if_nonexistant(file3, "5")
        with open('/'.join(file1), "r") as limit_file:
            message_limit = limit_file.read().strip()
            limit_file.close()
        with open('/'.join(file2), "r") as limit_file:
            art_limit = limit_file.read().strip()
            limit_file.close()
        with open('/'.join(file3), "r") as limit_file:
            gen_limit = limit_file.read().strip()
            limit_file.close()
        return [message_limit, art_limit, gen_limit]
    
    def get_usage(id):
        id = str(id)
        file1 = ["database", "limits", id, "messages", "usage"]
        file2 = ["database", "limits", id, "art", "usage"]
        file3 = ["database", "limits", id, "backstory", "usage"]
        database.create_if_nonexistant(file1, "0")
        database.create_if_nonexistant(file2, "0")
        database.create_if_nonexistant(file3, "0")
        with open('/'.join(file1), "r") as limit_file:
            message_limit = limit_file.read().strip()
            limit_file.close()
        with open('/'.join(file2), "r") as limit_file:
            art_limit = limit_file.read().strip()
            limit_file.close()
        with open('/'.join(file3), "r") as limit_file:
            gen_limit = limit_file.read().strip()
            limit_file.close()
        return [message_limit, art_limit, gen_limit]
    
    def enable_channel(id, client_id):
        id = str(id)
        client_id = str(client_id)
        file = ["database", "clients", client_id, "channels", id]
        database.create_if_nonexistant(file)
        with open('/'.join(file), "w") as limit_file:
            limit_file.close()

    def disable_channel(id, client_id):
        id = str(id)
        client_id = str(client_id)
        file = ["database", "clients", client_id, "channels", id]
        database.create_if_nonexistant(file)
        if os.path.exists('/'.join(file)):
            os.remove('/'.join(file))

    def is_enabled(id, client_id):
        id = str(id)
        client_id = str(client_id)
        file = ["database", "clients", client_id, "channels", id]
        return os.path.exists('/'.join(file))
    
    def is_limited(author):
        author = str(author)
        file = ["database", "limits", author, "messages", "max"]
        file1 = ["database", "limits", author, "messages", "usage"]
        database.create_if_nonexistant(file, "50")
        database.create_if_nonexistant(file1, "0")
        max = int(open('/'.join(file)).read().replace("\n", ""))
        used = int(open('/'.join(file1)).read().replace("\n", ""))
        return used >= max


    def is_art_limited(author):
        author = str(author)
        file = ["database", "limits", author, "art", "max"]
        file1 = ["database", "limits", author, "art", "usage"]
        database.create_if_nonexistant(file, "5")
        database.create_if_nonexistant(file1, "0")
        max = int(open('/'.join(file)).read().replace("\n", ""))
        used = int(open('/'.join(file1)).read().replace("\n", ""))
        return used >= max

    def log_msg(msg_id, client_id, channel_id, author, count=0):
        msg_id = str(msg_id)
        client_id = str(client_id)
        channel_id = str(channel_id)
        author = str(author)
        file = ["database", "clients", client_id, "channel_messages", channel_id, "messages", author]
        file1 = ["database", "limits", author, "messages", "usage"]
        database.create_if_nonexistant(file)
        database.create_if_nonexistant(file1, "0")
        with open('/'.join(file), "a") as file:
            file.write(msg_id + "\n")
            file.close()
        if count:
            with open('/'.join(file1), "r") as file_data:
                num = int(file_data.read().replace("\n", "")) + 1
                file_data.close()

            with open('/'.join(file1), "w") as file_data:
                file_data.write(str(num))
                file_data.close()

    def log_art(author, count=1):
        author = str(author)
        file1 = ["database", "limits", author, "art", "usage"]
        database.create_if_nonexistant(file1, "0")
        if count:
            with open('/'.join(file1), "r") as file_data:
                num = int(file_data.read().replace("\n", "")) + 1
                file_data.close()

            with open('/'.join(file1), "w") as file_data:
                file_data.write(str(num))
                file_data.close()


    def log_generation(author, count=1):
        author = str(author)
        file1 = ["database", "limits", author, "backstory", "usage"]
        database.create_if_nonexistant(file1, "0")
        if count:
            with open('/'.join(file1), "r") as file_data:
                num = int(file_data.read().replace("\n", "")) + 1
                file_data.close()

            with open('/'.join(file1), "w") as file_data:
                file_data.write(str(num))
                file_data.close()

    def is_generation_limited(author):
        author = str(author)
        file = ["database", "limits", author, "backstory", "max"]
        file1 = ["database", "limits", author, "backstory", "usage"]
        database.create_if_nonexistant(file, "5")
        database.create_if_nonexistant(file1, "0")
        max = int(open('/'.join(file)).read().replace("\n", ""))
        used = int(open('/'.join(file1)).read().replace("\n", ""))
        return used >= max

    def is_message(msg_id, client_id, channel_id, user_id):
        msg_id = str(msg_id)
        client_id = str(client_id)
        channel_id = str(channel_id)
        user_id = str(user_id)
        file = ["database", "clients", client_id, "channel_messages", channel_id, "messages", user_id]
        database.create_if_nonexistant(file)
        found = False
        with open('/'.join(file), "r") as file:
            for line in file:
                if line.replace("\n", "") == msg_id:
                    found = True
        return found
    

    def clear_channel(client_id, channel_id, user_id):
        user_id = str(user_id)
        client_id = str(client_id)
        channel_id = str(channel_id)
        file = ["database", "clients", client_id, "channel_messages", channel_id, "messages", user_id]
        # database.create_if_nonexistant(file)
        if os.path.exists('/'.join(file)):
            os.remove('/'.join(file))


    def enable_roleplay(client_id, user_id):
        client_id = str(client_id)
        user_id = str(user_id)
        file = ["database", "clients", client_id, "roleplay", user_id]
        database.create_if_nonexistant(file)
        # if os.path.exists('/'.join(file)):
        #     os.remove('/'.join(file))

    def disable_roleplay(client_id, user_id):
        client_id = str(client_id)
        user_id = str(user_id)
        file = ["database", "clients", client_id, "roleplay", user_id]
        # database.create_if_nonexistant(file)
        if os.path.exists('/'.join(file)):
            os.remove('/'.join(file))

    def is_roleplay_enabled(client_id, user_id):
        client_id = str(client_id)
        user_id = str(user_id)
        file = ["database", "clients", client_id, "roleplay", user_id]
        return os.path.exists('/'.join(file))
    
    def is_webhook_enabled(client_id, channel_id):
        client_id = str(client_id)
        channel_id = str(channel_id)
        file = ["database", "clients", client_id, "webhooks", channel_id]
        if os.path.exists('/'.join(file)):
            return open('/'.join(file)).read().replace("\n", "").strip()
        else:
            return False
        
    def enable_webhook(client_id, channel_id, url):
        client_id = str(client_id)
        channel_id = str(channel_id)
        file = ["database", "clients", client_id, "webhooks", channel_id]
        if os.path.exists('/'.join(file)):
            os.remove('/'.join(file))
        database.create_if_nonexistant(file, url)

    def disable_webhook(client_id, channel_id):
        client_id = str(client_id)
        channel_id = str(channel_id)
        file = ["database", "clients", client_id, "webhooks", channel_id]
        if os.path.exists('/'.join(file)):
            os.remove('/'.join(file))

    def add_memory(client_id, text):
        client_id = str(client_id)
        file = ["database", "clients", client_id, "memories"]
        database.create_if_nonexistant(file, "")
        with open('/'.join(file), "a") as file:
            file.write(text.replace("\n", "").strip() + "\n")

    def remove_memory(client_id, id):
        client_id = str(client_id)
        line_number = int(id.strip())
        file = ["database", "clients", client_id, "memories"]
        database.create_if_nonexistant(file, "")
        file_path = "/".join(file)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove the desired line
        if line_number >= 1 and line_number <= len(lines):
            del lines[line_number - 1]  # Adjust for 0-based indexing

            # Write the updated contents back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)

    def memories(client_id):
        client_id = str(client_id)
        file = ["database", "clients", client_id, "memories"]
        if os.path.exists('/'.join(file)):
            with open('/'.join(file)) as memory:
                data = [item for item in memory.read().split("\n") if item != '']
            return data
        else:
            return ""
        

    def set_language(user_id, language):
        user_id = str(user_id)
        file = ["database", "users", user_id, "language"]
        if os.path.exists('/'.join(file)): os.remove('/'.join(file))
        database.create_if_nonexistant(file, language)

    def get_language(user_id):
        user_id = str(user_id)
        file = ["database", "users", user_id, "language"]
        if os.path.exists('/'.join(file)):
            lang = open('/'.join(file)).read().strip().replace("\n", "")
        else:
            lang = "en"
        return lang
    
    def set_typing_style(user_id, typing_style):
        user_id = str(user_id)
        file = ["database", "users", user_id, "typing_style"]
        if os.path.exists('/'.join(file)): os.remove('/'.join(file))
        database.create_if_nonexistant(file, typing_style)

    def get_typing_style(user_id):
        user_id = str(user_id)
        file = ["database", "users", user_id, "typing_style"]
        if os.path.exists('/'.join(file)):
            typing_style = open('/'.join(file)).read().strip().replace("\n", "")
        else:
            typing_style = "none"
        return typing_style
    

    def set_enforced_typing_style(user_id, typing_style):
        user_id = str(user_id)
        file = ["database", "clients", user_id, "enforce_typing_style"]
        if os.path.exists('/'.join(file)): os.remove('/'.join(file))
        database.create_if_nonexistant(file, typing_style)

    def get_enforced_typing_style(user_id):
        user_id = str(user_id)
        file = ["database", "clients", user_id, "enforce_typing_style"]
        if os.path.exists('/'.join(file)):
            typing_style = open('/'.join(file)).read().strip().replace("\n", "")
        else:
            typing_style = "none"
        return typing_style

    def set_user_font(user_id, shape_id, charset):
        user_id = str(user_id)
        shape_id = str(shape_id)
        file = ["database", "clients", shape_id, "font", user_id]
        if os.path.exists('/'.join(file)): os.remove('/'.join(file))
        database.create_if_nonexistant(file, charset)

    def get_user_font(user_id, shape_id):
        user_id = str(user_id)
        shape_id = str(shape_id)
        file = ["database", "clients", shape_id, "font", user_id]
        if os.path.exists('/'.join(file)):
            typing_style = open('/'.join(file)).read().strip().replace("\n", "")
        else:
            typing_style = "none"
        return typing_style

    def set_user_ignore(user_id, timestamp):
        user_id = str(user_id)
        timestamp = str(timestamp)
        file = ["database", "users", user_id, "ignore"]
        if os.path.exists('/'.join(file)): os.remove('/'.join(file))
        database.create_if_nonexistant(file, timestamp)
        with open('/'.join(file), "w") as file:
            file.write(timestamp)
            file.close()

    def ignore_user(user_id):
        user_id = str(user_id)
        file = ["database", "users", user_id, "ignore"]
        if os.path.exists('/'.join(file)):
            typing_style = open('/'.join(file)).read().strip().replace("\n", "")
        else:
            return False
        return float(typing_style) > time.time()