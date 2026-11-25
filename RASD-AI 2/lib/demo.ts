import type { Zone, ForecastResult, SimulationRequest, SimulationResult } from './types';
const base = [28,32,36,39,45,51,59,66,72,80,88,92];
const times = base.map((_,i)=>`${String(9+Math.floor(i/6)).padStart(2,'0')}:${i%6}0`);
const series = (offset:number,scale:number)=>base.map((n,i)=>({time:times[i],value:Math.round(n*scale+offset)}));
export const demoZones: Zone[] = [
 {id:'north',name:'المدخل الشمالي',people:184,density_level:'medium',density_score:55,updated_at:'بيانات توضيحية',history:series(0,0.6)},
 {id:'east',name:'الممر الشرقي',people:312,density_level:'high',density_score:86,updated_at:'بيانات توضيحية',history:series(8,0.88)},
 {id:'west',name:'الممر الغربي',people:98,density_level:'low',density_score:24,updated_at:'بيانات توضيحية',history:series(-5,0.38)},
 {id:'south',name:'المدخل الجنوبي',people:226,density_level:'medium',density_score:63,updated_at:'بيانات توضيحية',history:series(5,0.7)},
 {id:'central',name:'الساحة المركزية',people:415,density_level:'high',density_score:91,updated_at:'بيانات توضيحية',history:series(14,1)},
 {id:'exit',name:'منطقة الخروج',people:76,density_level:'low',density_score:19,updated_at:'بيانات توضيحية',history:series(-8,0.33)},
];
export function demoForecast(zoneId:string,horizon:number):ForecastResult {const z=demoZones.find(x=>x.id===zoneId)||demoZones[0];return {zone_id:z.id,observed:z.history,predicted:[],confidence:null,horizon_minutes:horizon,source:'demo',sufficient_data:false};}
export function demoSimulate(input:SimulationRequest):SimulationResult { const z=demoZones.find(x=>x.id===input.zone_id)||demoZones[0];const initial=Math.max(0,input.initial_people);const baseline=Array.from({length:input.duration_minutes+1},(_,minute)=>({minute,people:Math.max(0,Math.round(initial+minute*(z.density_score/35-1.3)))}));const scenario=Array.from({length:input.duration_minutes+1},(_,minute)=>({minute,people:Math.max(0,Math.round(initial+minute*(input.entry_rate-input.exit_rate)))}));return {baseline,scenario,source:'demo',disclaimer:'نموذج حسابي توضيحي يعتمد على صافي الدخول والخروج، وليس توقعًا علميًا أو توصية ميدانية.'}; }
