import codecs
from poesy import Poem

def product(*args):
    if not args:
        return iter(((),)) # yield tuple()
    return (items + (item,)
        for items in product(*args[:-1]) for item in args[-1])


def scheme2edges(scheme):
    id2pos={}
    for i,x in enumerate(scheme):
        # x is a rhyme id, i is the position in the scheme
        if x==0: continue
        if not x in id2pos: id2pos[x]=[]
        id2pos[x]+=[i]

    rhymes=[]
    for x in id2pos:
        if len(id2pos[x])>1:
            for a,b in product(id2pos[x], id2pos[x]):
                if a>=b: continue
                rhymes+=[(a,b)]
    return rhymes

def do_get_feats(fn):
    print '>>',fn,'...'
    try:
        with codecs.open(fn,encoding='utf-8') as f: txt=f.read()
        poem=Poem(txt)
        statd=poem.statd
        statd['fn']=fn
        
        # convert list to feats
        if statd['rhyme_schemes']:
           for (schemename,schemevals),acc in statd['rhyme_schemes']:
               statd['rhyme_scheme_acc_'+schemename]=acc
        del statd['rhyme_schemes']
        
        for l1,l2 in sorted(scheme2edges(poem.rhyme_ids)):
            statd['rhymes_l{0}-l{1}'.format(str(l1+1).zfill(2),str(l2+1).zfill(2))]=1
        return statd
    except AttributeError:
        return {}