
from godcomplex import World
from godcomplex import PrintUtil
import numpy
from PIL import Image
import sqlite3

MAX_HISTORY_SHOWN = 30

if __name__ == '__main__':
    db = sqlite3.connect('file:worldgen.db?mode=ro', uri=True)
    world = World(db=db)

    print('Generating terrain...')
    world.init_terrain()
    PrintUtil.print_terrain(world)
    print('========================')

    print('Generating moisture...')
    world.init_moisture()
    PrintUtil.print_digit_layer(world, 'moisture')
    print('========================')

    print('Generating biomes...')
    world.init_biomes()
    PrintUtil.print_terrain(world)
    print('========================')

    print('Generating peoples...')
    world.init_peoples()
    print('========================')

    print('The world has started. Input newline to run a single simulation step.')

    current_view = 'activity'
    while True:
        print('Currently in {} view. '.format(current_view) +
              'Commands: [ag]ent list, [se]ttlement list, [f]action list, [h]istorical events, [a]ctivity view, [t]errain view, [g]reyscale export' +
              '\033[0J')
        cmd = input()
        results = None
        if cmd.startswith('ag'):
            print('\n'.join([str(a) for a in world.agents.values()]))
            input()
        elif cmd.startswith('se'):
            print('\n'.join([str(a) for a in world.agents.values() if a.agent_type == 'SETTLEMENT']))
            input()
        elif cmd.startswith('h'):
            print('\n'.join([str(e) for e in world.history.events[-MAX_HISTORY_SHOWN:]]))
            input()
        elif cmd.startswith('f'):
            print('\n'.join([str(a) for a in world.factions.values()]))
            input()
        elif cmd.startswith('a'):
            current_view = 'activity'
        elif cmd.startswith('t'):
            current_view = 'terrain'
        elif cmd.startswith('g'):
            Image.fromarray(numpy.asarray(world.elevation) * 255) \
                .convert('RGB') \
                .save('test.bmp')
        else:
            results = world.step()

        print('\033[;HYear {}, First Age of the World\033[0K'.format(
            world.history.current_timestamp))
        if current_view == 'activity':
            PrintUtil.print_activity(world)
        elif current_view == 'terrain':
            PrintUtil.print_terrain(world)
        if results is not None:
            for result in results:
                print(result.pretty_str())
