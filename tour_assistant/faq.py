from .root import app

SEASONAL_NOTE = 0

@app.handle(intent='facilities')
def inform_facilities(request, responder):
    responder.reply('You will find water fountains, restrooms, maps and area information, and Parkway keepsakes at Visitor Centers.')
    responder.reply('Milepost 5.8 - Humpback Rocks\n'
    				'Milepost 63.6 - James River\n'
    				'Milepost 86 – Peaks of Otter\n'
					'Milepost 115 – Explore Park\n'
					'Milepost 169 – Rocky Knob\n'
					'Milepost 213 – Blue Ridge Music Center\n'
					'Milepost 241 – Doughton Park\n'
					'Milepost 294.1 – Moses H. Cone\n'
					'Milepost 304.4 – Linn Cove Viaduct\n'
					'Milepost 316.4 – Linville Falls\n'
					'Milepost 331 – Museum of NC Minerals\n'
					'Milepost 364.6 – Craggy Gardens\n'
					'Milepost 382 – Folk Art Center\n'
					'Milepost 384 – The Blue Ridge Parkway Visitor Center\n'
					'Milepost 451.2 – Waterrock Knob')
    # the following notes just need to tell once
    global SEASONAL_NOTE
    if not SEASONAL_NOTE:
    	responder.reply('Most facilities like Visitor Centers, picnic areas, and campgrounds on the Parkway operate on a seasonal basis – please note this includes restrooms and plan accordingly.')
    	responder.reply('Facilities that are open year-round are: the NC Museum of Minerals, the Folk Art Center, the Blue Ridge Parkway Visitor Center in Asheville, NC, and the Price Park Picnic Area. In winter, sections of the Parkway may be closed by snow or ice.')
    	SEASONAL_NOTE = 1

@app.handle(intent='detours_and_closings')
def show_closure_map(request, responder):
	responder.reply('The most up to date closing information about the Blue Ridge Parkway can be accessed by viewing the Real-Time Road Closure Map: go.nps.gov/brp-map')

@app.handle(intent='tunnel_clearance')
def show_tunnel_clearance(request, responder):
	responder.reply('There are no special permits are required for tour buses and large RV\'s.'
					'Please review the tunnel clearance information: https://www.blueridgeparkway.org/tunnels/')

@app.handle(intent='speed_limit')
def check_speed_limit(request, responder):
	responder.reply('Maximum is 45 miles per hour, with some locations (in congested areas such as Mabry Mill) at 25 miles per hour.')
