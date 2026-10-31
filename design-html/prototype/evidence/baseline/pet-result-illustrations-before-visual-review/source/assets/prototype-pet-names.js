/* Resolve original UI name templates once, without reinterpreting user/controller-owned content. */
(() => {
  const hasName=/糯米|小满|阿舟/,tokens=/糯米|小满|阿舟/g;
  let templates=null;
  function capture(){
    const items=[];
    for(const element of document.querySelectorAll('title,h1,h2,p,span,strong,small,button,nav')){
      for(const node of element.childNodes)if(node.nodeType===Node.TEXT_NODE&&hasName.test(node.nodeValue))items.push({node,attribute:null,template:node.nodeValue,last:node.nodeValue,active:true});
    }
    for(const node of document.querySelectorAll('[aria-label],[alt],[title]'))for(const attribute of ['aria-label','alt','title']){
      const value=node.getAttribute(attribute);if(value&&hasName.test(value))items.push({node,attribute,template:value,last:value,active:true});
    }
    return items;
  }
  function paint({pet,actor,peer}){
    if(!templates)templates=capture();
    const names={'糯米':String(pet),'小满':String(actor),'阿舟':String(peer)};
    for(const item of templates){
      if(!item.active||!item.node.isConnected)continue;
      const current=item.attribute?item.node.getAttribute(item.attribute):item.node.nodeValue;
      // A later controller update owns that value. Never rewrite it as an old source template.
      if(current!==item.last){item.active=false;continue;}
      const next=item.template.replace(tokens,key=>names[key]);
      if(item.attribute)item.node.setAttribute(item.attribute,next);else item.node.nodeValue=next;
      item.last=next;
    }
  }
  window.PrototypePetNames={paint};
})();
