/* ---------- the cast: one entry per person per era. Families share features. ---------- */
const NAVY = '#2c3644', CHAR = '#30333a';
const CAST = {
  saku:     { name: '三雲 朔', role: '霧渕署 刑事', sex: 'm', age: 38, hs: 'messy', scar: 1, beard: 'stubble', brow: 1.15, hair: '#2b2530', eye: '#5b4636', cloth: { t: 'coat', c: '#44546f', tie: '#7a2f38' }, wet: 1 },
  akari:    { name: '朽木 灯', role: '霧渕署 鑑識', sex: 'f', age: 31, hs: 'tied', es: 1.06, hair: '#3a2a26', eye: '#8a5a30', cloth: { t: 'work', c: '#2f6aa3', tag: '鑑識' } },
  rei:      { name: '鷹取 玲', role: '霧渕原発 所長', sex: 'f', age: 41, hs: 'bob', es: .9, tilt: 2.2, nose: 1.06, fw: .97, hair: '#231f2b', eye: '#4d5f78', cloth: { t: 'suit', c: '#46405a', tie: '#a03a48' } },
  seiji76:  { name: '鷹取 征二', role: '鷹取家 当主', sex: 'm', age: 76, hs: 'back', grey: .92, es: .88, tilt: 2.4, nose: 1.12, fw: .97, jaw: .5, eye: '#4d5f78', cloth: { t: 'suit', c: '#3b3a45', tie: '#8a6a2a' } },
  seiji43:  { name: '鷹取 征二', role: '霧渕原発 副所長', sex: 'm', age: 43, hs: 'back', grey: .12, es: .88, tilt: 2.4, nose: 1.12, fw: .97, jaw: .5, recede: 0, hair: '#231f2b', eye: '#4d5f78', cloth: { t: 'suit', c: '#4a5266', tie: '#a03a48' } },
  seiji10:  { name: '鷹取 征二', role: '鷹取組の子', sex: 'm', age: 10, hs: 'bowl', es: .92, tilt: 2, hair: '#231f2b', eye: '#4d5f78', cloth: { t: 'gakuran', c: '#2c2f3a' } },
  sayo58:   { name: '朽木 小夜', role: '朽木屋 女将', sex: 'f', age: 58, hs: 'bun', grey: .35, hair: '#3a2a26', eye: '#8a5a30', cloth: { t: 'kimono', c: '#5b6590' } },
  sayo25:   { name: '朽木 小夜', role: '朽木屋の娘', sex: 'f', age: 25, hs: 'tied', hair: '#3a2a26', eye: '#8a5a30', cloth: { t: 'kimono', c: '#c4667a', apron: 1 } },
  osamu71:  { name: '汐見 修', role: '汐見医院 院長', sex: 'm', age: 71, hs: 'thin', grey: .85, glasses: 'round', tilt: -2, jaw: .3, eye: '#3f6b5a', cloth: { t: 'labcoat', tie: '#3f6a8a' } },
  osamu38:  { name: '汐見 修', role: '汐見医院 医師', sex: 'm', age: 38, hs: 'short', glasses: 'round', tilt: -2, jaw: .3, hair: '#33282a', eye: '#3f6b5a', cloth: { t: 'labcoat', tie: '#3f6a8a' } },
  ren27:    { name: '汐見 蓮', role: '霧渕原発 技師', sex: 'm', age: 27, hs: 'short', mole: 1, tilt: -2, jaw: .3, brow: .85, hair: '#33282a', eye: '#3f6b5a', cloth: { t: 'work', c: '#5f7f96', tag: '霧渕原発' } },
  tadashi27:{ name: '匡', role: '記憶のない青年', sex: 'm', age: 27, hs: 'short', mole: 1, tilt: -2, jaw: .3, brow: .85, hair: '#33282a', eye: '#3f6b5a', cloth: { t: 'knit', c: '#8a7a55' } },
  tadashi60:{ name: '朽木 匡', role: '朽木屋 主人', sex: 'm', age: 60, hs: 'short', grey: .6, mole: 1, tilt: -2, jaw: .3, brow: .85, hair: '#33282a', eye: '#3f6b5a', cloth: { t: 'work', c: '#6b7a55' } },
  iwao35:   { name: '三雲 巌', role: '霧渕署 巡査部長', sex: 'm', age: 35, hs: 'short', brow: 1.2, hair: '#2b2530', eye: '#5b4636', cap: '#33415e', cloth: { t: 'uniform', c: '#3a4a6e', tie: '#22283a' } },
  kiichi35: { name: '三雲 喜一', role: '霧渕駐在所 巡査', sex: 'm', age: 35, hs: 'buzz', brow: 1.2, beard: 'mustache', hair: '#2b2530', eye: '#5b4636', cap: '#2c3040', cloth: { t: 'uniform', c: '#343a4e', tie: '#1e2230' } },
  haru40:   { name: '朽木 ハル', role: '朽木屋 女将', sex: 'f', age: 40, hs: 'bun', hair: '#3a2a26', eye: '#8a5a30', cloth: { t: 'kimono', c: '#8a6a4a', apron: 1 } },
  soichiro45:{ name: '鷹取 宗一郎', role: '鷹取組 社長', sex: 'm', age: 45, hs: 'buzz', es: .88, tilt: 2.4, nose: 1.12, fw: 1, jaw: .75, beard: 'mustache', hair: '#231f2b', eye: '#4d5f78', cloth: { t: 'work', c: '#7a6a45', tag: '鷹取組' } },
  kid5:     { name: '三雲 朔', role: '5歳', sex: 'm', age: 5, hs: 'bowl', hair: '#2b2530', eye: '#5b4636', cloth: { t: 'knit', c: '#c9a04e' } },
  toki74:   { name: 'トキ', role: '鷹取家のばあや', sex: 'f', age: 74, hs: 'bun', grey: .8, es: .9, tilt: 2.2, nose: 1.06, fw: .97, hair: '#231f2b', eye: '#4d5f78', cloth: { t: 'kimono', c: '#5a5560', apron: 1 } },
  rei8:     { name: '鷹取 玲', role: '8歳', sex: 'f', age: 8, hs: 'bob', es: .95, tilt: 2, hair: '#231f2b', eye: '#4d5f78', cloth: { t: 'knit', c: '#d98aa0' } },
  nozomu5:  { name: '男の子', role: '5つくらい', sex: 'm', age: 5, hs: 'bowl', hair: '#2b2530', eye: '#5b4636', cloth: { t: 'knit', c: '#5f8fb8' } },
  tae30:    { name: '汐見 多恵', role: '産婆', sex: 'f', age: 30, hs: 'shortf', tilt: -2, hair: '#33282a', eye: '#3f6b5a', cloth: { t: 'labcoat' } },
};
if (typeof module !== 'undefined') module.exports = { CAST };
