# TeamLocker Products

TeamLocker is a project which will (eventually) have three distinct products/outputs all available on PyPI via `pip3 install teamlocker`.

1. A standalone server `teamlockerd`, probably in PEX format.
1. A standalone command-line client `teamlocker`, also probably in PEX format.
1. A client library `teamlocker` that can be imported into projects that want to use the teamlocker backend.

# Scenario

TeamLocker is an invitation-based, data-hosting service for sharing your structured data with friends. In this imaginary dialogue with a command-line client, we indirectly explain how it works and what it can do. It's a nice easy way to understand what is happening. But, to be clear, TeamGroove would use a Python library rather than a command-line client.

```
% teamlocker
Thanks for installing TeamLocker, the online structured data hosting service. Create new lockers
with the --new-locker option, upload files with the --upload-file option, and invite friends to
share lockers with the --invite option. If you want a summary of commands please use the --help
option. 

P.S. Your locker keys are stored in the folder ~/.config/teamlocker. Your data is only as secure 
as your keys, so never share them; they won't work on other machines anyway!

% teamlocker --new-locker 'Awesome Mix Tape (Vols 1 & 2)'
Locker "Awesome Mix Tape (Vols 1 & 2)" created. Nice!

% teamlocker --mkdir 'Drafts' --locker 'Awesome Mix Tape (Vols 1 & 2)'
Folder 'Drafts' created in locker "Awesome Mix Tape (Vols 1 & 2)". Lookin' good!

% teamlocker --upload mixtape.sqlite3 --to Drafts/MixTape1 --locker 'Awesome Mix Tape (Vols 1 & 2)'
New SQLITE3 file 'MixTape1' added to folder 'Drafts' in locker "Awesome Mix Tape (Vols 1 & 2)". Good job!
```

And we can upload from stdin:

```
% teamlocker --upload=- --type=json --to=Drafts/MixTape2 --locker='Awesome Mix Tape (Vols 1 & 2)' << EOF
[
    { "title": "Ain't No Mountain High Enough", "by": "Marvin Gaye and Tammi Terrell" },
    { "title": "I Want You Back", "by": "The Jackson 5" },
    { "title": "Mr. Blue Sky", "by": "Electric Light Orchestra" },
    { "title": "Fox on the Run", "by": "Sweet" },
    { "title": "Lake Shore Drive", "by": "Aliotta Haynes Jeremiah" },
    { "title": "The Chain", "by": "Fleetwood Mac" },
    { "title": "Bring It On Home to Me", "by": "Sam Cooke" },
    { "title": "Southern Nights", "by": "Glen Campbell" },
    { "title": "My Sweet Lord", "by": "George Harrison" },
    { "title": "Brandy (You're a Fine Girl)", "by": "Looking Glass" },
    { "title": "Come a Little Bit Closer", "by": "Jay and the Americans" },
    { "title": "Wham Bam Shang-A-Lang", "by": "Silver" },
    { "title": "Surrender", "by": "Cheap Trick" },
    { "title": "Father and Son", "by": "Cat Stevens" },
    { "title": "Flash Light", "by": "Parliament" },
    { "title": "Guardians' Inferno", "by": "The Sneepers featuring David Hasselhoff" }
]
EOF
% 
```

```
% teamlocker --invite funkhound@mail.com --valid-hours 48 --role=read-only --locker 'Awesome Mix Tape (Vols 1 & 2)' --verbose
Sending email to funkhound@mail.com ... sent. This invitation code is valid for 48 hours:
################################################################################
# TeamLocker invitation 
# 7B2274797065223A225465616D4C6F636B6572496E7669746174696F6E222C202256616C696455
# 6E74696C223A22323032322D30332D30313A31333A32343A3433222C22436F6465223A226B7375
# 636E686B62636B7574346236657436773733786977796269797577777579696777786777796720
# 72773634363737363435373634747572796734337274373467727975333767227D
################################################################################
% 
```

When _Funkhound_ picks up the invitation, they can accept it and get access to the locker:
```
% teamlocker --review-invitation 
Please enter the invitation:
################################################################################
# TeamLocker invitation 
# 7B2274797065223A225465616D4C6F636B6572496E7669746174696F6E222C202256616C696455
# 6E74696C223A22323032322D30332D30313A31333A32343A3433222C22436F6465223A226B7375
# 636E686B62636B7574346236657436773733786977796269797577777579696777786777796720
# 72773634363737363435373634747572796734337274373467727975333767227D
################################################################################

This is a read-only invitation to locker "Awesome Mix Tape (Vols 1 & 2)", 
generated today and valid for another 44 hours. 
"Awesome Mix Tape (Vols 1 & 2)"
Would you like to 
a) Accept the invitation?
r) Request a different role?
v) Verify the sender?
? a

Accepted! You have read-only access to locker "Awesome Mix Tape (Vols 1 & 2)"
```

_Funkhound_ can now continue working with the locker files:
```
% teamlocker --method=execute --argument='SELECT * FROM playlist' --file='Drafts/MixTape1' --locker='Awesome Mix Tape (Vols 1 & 2)'
[
    { "title": "Come and get your love", "at": "00:00" },
    { "title": "I want you back", "at": "03:31" },
    { "title": "Spirit in the sky", "at": "06:29" },
    { "title": "Hooked on a feeling", "at": "10:31" },
    { "title": "Escape (The Pina Colada Song)", "at": "13:25" },
    { "title": "O-o-h Child", "at": "17:37" },
    { "title": "Ain't No Mountain High Enough", "at": "20:51" },
    { "title": "I'm Not In Love", "at": "23:18" },
    { "title": "Fooled Around And Fell In Love", "at": "29:17" },
    { "title": "Go All the Way", "at": "32:17" },
    { "title": "Moonage Daydream", "at": "35:19" },
    { "title": "Cherry bomb", "at": "40:19" },
    { "title": "Wham Bam Shang-A-Lang", "at": "42:39" },
    { "title": "Fox on the run", "at": "46:13" },
    { "title": "Mr. Blue Sky", "at": "49:38" }
]
```

And list the contents of folders:
```
teamlocker --list --path=Drafts --locker='Awesome Mix Tape (Vols 1 & 2)'
[
    { "name": "MixTape1", "type": "sqlite3" },
    { "name": "MixTape2", "type": "json" } 
]
```

And use smart queries/updates:
```
% teamlocker --method=jq --command='.[].by' --locker='Awesome Mix Tape (Vols 1 & 2)'
[
  "Marvin Gaye and Tammi Terrell",
  "The Jackson 5",
  "Electric Light Orchestra",
  "Sweet",
  "Aliotta Haynes Jeremiah",
  "Fleetwood Mac",
  "Sam Cooke",
  "Glen Campbell",
  "George Harrison",
  "Looking Glass",
  "Jay and the Americans",
  "Silver",
  "Cheap Trick",
  "Cat Stevens",
  "Parliament",
  "The Sneepers featuring David Hasselhoff"
]
% 
```


# Original Motivation

While working on TeamGroove I became quietly interested with the idea of an invitation-based, rather than registration-based, RESTful hierarchical structured-file store. The central idea is that someone who 'owns' a folder in the store can invite other people to the folder or any sub-folder. These invitations would arrive by (say) email and the recipient could enter that invitation into TeamGroove Console and immediately join the team without any apparent registration.

Aside: The files would be 'structured' in the sense that they would support queries/updates, not just entire downloads and uploads. A bit like PROPFIND/PROPPATCH for WebDAV only with operations that were specific to particular file types. An example would be SQLITE3 files and the queries/updates are SQL. Another example would be JSON and queries via `jq`.
