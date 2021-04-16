import utils, os


# input
app_name= input("app name: ")

# new directories
base= os.path.join(utils.WEBVIEW_DIR, app_name) + os.path.sep
assert not os.path.exists(base), f"App already exists: {base}"

new_dirs= ["css", "js", "templates"]
new_dirs= [base] + [base + x for x in new_dirs]

# new files (file_name : content)
new_files= {}

new_files[base + '__init__.py']= ""
new_files[base + 'urls.py']= ""
new_files[base + 'views.py']= ""

# create
for x in new_dirs:
	print(f"creating {x.replace(base, os.path.sep)}")
	os.mkdir(x)

for x,y in new_files.items():
	print(f"creating {x.replace(base, os.path.sep)}")
	with open(x, "w") as file:
		file.write(y)