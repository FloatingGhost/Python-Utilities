var spr_ai = {

spr:null,
alive:false,
  phases:[
  function() {
if (this.alive) return;
  this.alive = true; 
  console.log('Beginning Attack_Phase');
  game.add.tween(spr).to({x:spr.x+100, y:spr.y+200}, 3000).start();
  
  game.time.events.add(Phaser.Timer.SECOND * 3,   function() {

;
  game.add.tween(spr).to({x:spr.x+-100, y:spr.y+-200}, 3000).start();
  
  game.time.events.add(Phaser.Timer.SECOND * 3,   function() {

;
    spr.rotation = -1;
  
  game.time.events.add(Phaser.Timer.SECOND * 3,   function() {

;
    spr.rotation = 0;
  
  game.time.events.add(Phaser.Timer.SECOND * 3,   function() {

;
  game.add.tween(spr).to({x:spr.x+-100, y:spr.y+100}, 3000).start();
  
  game.time.events.add(Phaser.Timer.SECOND * 3,   function() {

;

this.alive=false;
}, this)}, this)}, this)}, this)}, this)},

],
 setup_spr_ai: function(object) {
  spr = object;
},

update:function(){
  if (!this.alive) {
  var index = Math.floor(Math.random() * this.phases.length);
  var func = this.phases[index]
  
  func();  
}},
}