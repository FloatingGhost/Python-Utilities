#!/usr/bin/env python3

__package__ = "floatingutils.games"
__author__ = "Hannah Ward"


##############
#games.ai    #
#Parser for  #
#Phaser.io AI#
##############


import json
import argparse
import re
from floatingutils.log import Log

log = Log()

log.debug("Initialising Parser...")
parser = argparse.ArgumentParser(description='Parse a .ai file into JSON')
parser.add_argument("filename", help="The .ai file to process")
parser.add_argument('--game', default="game",
                   help='The name of your \'game\' instance - usually just game')

parser.add_argument('--obj', help="The game of your game object that the AI will apply to")
parser.add_argument("--varname", help="The variable name to be output", default="ai")
parser.add_argument("--out", default="ai.out", help="The output filename")
log.debug("Parser ready")

args = parser.parse_args()

log.info("Processing {}".format(args.filename))
log.info("Using game instance {}".format(args.game))
obj = args.obj or "obj"
log.info("Using in-game instance {}".format(obj))


class AI:
  def __init__(self, game_inst, object_name, aidata):
    log.info("Initialising AI Class ({}.{})...".format(game_inst, object_name)) 
    self.aidata = [x.strip() for x in aidata if x != "\n" and x != '']
    
    self.breakarr = [] 
    self.breaks = 0
    self.game_inst = game_inst
    self.object_name = object_name 
    self.compile_regex()
    self.phases = {} 
    self.process_data()
    log.info("AI File parsed succesfully")

  def compile_regex(self):
    log.info("Compiling regular expressions...")
    self.re_phase = re.compile("\[[A-Za-z0-9_]*\]")
  
  def process_data(self):
    log.info("AI processing...")
    log.line()
    log.incIndent()
    for line in self.aidata:
      if self.re_phase.match(line):
        try:
          log.info(self.phases[phase_name])
          log.info("Pushing {}".format(self.breaks))
          self.breakarr.append(self.breaks)
          self.breaks = 0
        except:
          pass
        log.line("-")
        phase_name = line[1:-1]
        log.info("Detected phase {}".format(phase_name)) 
        self.phases[phase_name] = []
        log.line("-")
      else:
        p = (self.Phase(phase_name, line, self.breaks))
        self.breaks = p.breaks
        p = str(p)
        self.phases[phase_name].append(p)
    log.decIndent()
    log.line()
    self.breakarr.append(self.breaks)
  def __repr__(self):
    a = "  phases:[\n".format(args.varname)
    for i in self.phases:
      x = "  function() {{\nif (this.alive) return;\n".format(obj)
      x += "  this.alive = true; \n  console.log('Beginning {}');\n".format(i);
      for j in self.phases[i]:
        x += "  " + j + ";\n"
      a += x + "\nthis.alive=false;\n{}}},\n".format("}, this)"*self.breakarr.pop())
    a+= "\n],"
    return a
     
  class Phase:
    def __init__(self, phasename, phaseinfo, brks):
      
      self.breaks = brks
      self.phaseinfo = self.process(self.tokenise(phaseinfo))
      self.phasename = phasename

    def process(self, tokens):
      if tokens[0] == "set":
        ##Magic memes
        return "  {}.{} = {}".format(obj, tokens[1], tokens[2])
      else:
        if len(tokens) == 1:
          tokens.append("")
        if tokens[0] == "move":
          return "{}.add.tween({}).to({{x:{}.x+{}, y:{}.y+{}}}, {}).start()".format(
            args.game, obj, obj, tokens[1], obj, tokens[2], tokens[3])
        if tokens[0] == "wait":
          log.info("BREAK DETECTED {}".format(self.breaks))
          x = "  function() {{\n".format("update", self.breaks,self.breaks);
          self.breaks += 1
          return """\n  {0}.time.events.add(Phaser.Timer.SECOND * {1}, {3}\n""".format(args.game, int(tokens[1]), "{}_{}".format("update", self.breaks-1),x)
        return "{}.{}({})".format(obj, tokens[0], ",".join(tokens[1:]))

    def tokenise(self, info):
      return info.split(" ")

    def __repr__(self):
      return str(self.phaseinfo)

try:
  with open(args.filename, "r") as f:
    data = f.read()
except FileNotFoundError:
  log.error("Could not find file {} -- Make sure it exists".format(args.filename))

ai = AI(args.game, obj, data.split("\n"))

updatefunc = """\n setup_{0}_ai: function(object) {{
  {0} = object;
}},

update:function(){{
  if (!this.alive) {{
  var index = Math.floor(Math.random() * this.phases.length);
  var func = this.phases[index]
  
  func();  
}}}},""".format(obj, args.varname)

with open(args.out, "w") as f:
  f.write("var {}_ai = {{\n".format(obj))
  f.write("\n{}:null,\nalive:false,\n".format(obj))
  f.write(str(ai))
  f.write(updatefunc)
  f.write("\n}")
