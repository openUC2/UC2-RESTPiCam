#%%
from restpicamera import client as camera

#%%
rccamera = camera.restpicamera(host, port)
print(rccamera.get_iso())
print(rccamera.get_snap())
# %%
import pkgutil

# this is the package we are inspecting -- for example 'email' from stdlib
import restpicamera

package = restpicamera
for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
    print("Found submodule %s (is a package: %s)" % (modname, ispkg))