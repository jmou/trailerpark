import os

steps = []

for i, url in enumerate(open('in/urls')):
    url = url.strip()
    step = f'{i:08d}'
    steps.append(step)
    print(f'_pos={step}-steps')
    print('process=command:chmod +x in/template && '
          'mkdir out/files && '
          'cp -R in/imdb_url in/store/ in/modules/ out/files/ && '
          'in/template in/raw in out/files . $(<in/target) in/imdb_url=file:imdb_url in/store/=file:store/ in/modules/=file:modules/ > out/plan')
    for dirpath, _, filenames in os.walk('inref/phase2'):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            with open(filepath) as reffh:
                cid = reffh.read().strip()
            suffix = filepath[13:]
            print(f'in/{suffix}={cid}')
    print(f'in/imdb_url=inline:{url}')
    print()

    print(f'_pos={step}')
    print('process=dynamic')
    print(f'in/=_pos:{step}-steps:out/')
    print()

print('_pos=main')
print('process=command:ls in/* | sort | xargs cat > out/index.html')
for step in steps:
    print(f'in/{step}=_pos:{step}:out/makefrag.py/-')
print()
