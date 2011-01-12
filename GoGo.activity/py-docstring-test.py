def f():
    """We have doc-strings :-)"""
    
if f.__doc__ == None:
    print "There are no doc-strings! :-("
else:
    print f.__doc__
