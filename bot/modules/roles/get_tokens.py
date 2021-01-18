async def get_tokens(self, msg: str):
        # .add [Member1, Member2, ...] [Roles1, Role2, ...]

        members = ''
        roles   = ''
        state   = 0
        for c in msg:
                if state == 0:
                        # Skip command chars until first [
                        if c == '[':
                                state = 1
                        continue

                if state == 1:
                        # we are gathering members
                        if c != ']':
                                members += c
                        else:
                                state = 2
                        continue

                if state == 2:
                        # we finished members, waiting for roles
                        if c == '[':
                                state = 3
                        continue

                if state == 3:
                        # we found our roles!
                        if c != ']':
                                roles += c
                        else:
                                break

        
        
	# members = msg.partition("] [")[0].strip()
	# members.split()[3:]

	# roles = msg.partition("] [")[2]
	# roles.split()[:-2]

	tokens = {
                "members": [x.strip() for x in members.split(',')],
                "roles":   [x.strip() for x in roles.split(',')  ], 
        }
	return tokens
