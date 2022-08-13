import inspect
import importlib
import sys
import importlib.util

# for other folders the path must be dotted ('dir1.dir2.file.py')
module = importlib.import_module("plugin")
# spec = importlib.util.find_spec("plugin")
# spec = importlib.util.spec_from_file_location(module_name, file_path)
# module = importlib.util.module_from_spec(spec)
# sys.modules["plugin"] = module
# spec.loader.exec_module(module)

for name, obj in inspect.getmembers(module):
    print(f"name = {name}")
    if inspect.ismodule(obj):
        print("\tModule")
    if inspect.isclass(obj):
        print("\tClass")
        src = inspect.getsourcelines(obj)
        print(src)
    if inspect.ismethod(obj):
        print("\tMethod")
    if inspect.isfunction(obj):
        print("\tFunction")
    if inspect.isgeneratorfunction(obj):
        print("\tGenerator Function")
    if inspect.isgenerator(obj):
        print("\tGenerator")
    if inspect.iscoroutinefunction(obj):
        print("\tCoroutine Function")
    if inspect.iscoroutine(obj):
        print("\tCoroutine")
    if inspect.isawaitable(obj):
        print("\tAwaitable")
    if inspect.isasyncgenfunction(obj):
        print("\tAsync Gen Function")
    if inspect.istraceback(obj):
        print("\tTraceback")
    if inspect.isframe(obj):
        print("\tFrame")
    if inspect.iscode(obj):
        print("\tCode")
    if inspect.isbuiltin(obj):
        print("\tBuiltin")
    if inspect.isroutine(obj):
        print("\tRoutine")
    if inspect.isabstract(obj):
        print("\tAbstract")
    if inspect.ismethoddescriptor(obj):
        print("\tMethod Descriptor")
    if inspect.isdatadescriptor(obj):
        print("\tData Descriptor")
    if inspect.isgetsetdescriptor(obj):
        print("\tGet/Set Descriptor")
    if inspect.ismemberdescriptor(obj):
        print("\tMember Descriptor")
