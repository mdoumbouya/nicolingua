class TagEditor extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.state = { 
      value: 'Hello, **world**!',
      selectedTags: new Set()
    };
    
    this.tags =[
      {category:"language", tag:"lng-maninka", description:"maninka"},
      {category:"language", tag:"lng-susu", description:"susu"},
      {category:"language", tag:"lng-pular", description:"pular"},
      {category:"language", tag:"lng-koniaka", description:"koniaka"},
      {category:"language", tag:"lng-kisi", description:"kisi"},
      {category:"language", tag:"lng-guerze", description:"guerze"},
      {category:"language", tag:"lng-toma", description:"toma"},
      {category:"language", tag:"lng-kono", description:"kono"},
      {category:"language", tag:"lng-mano", description:"mano"},
      {category:"language", tag:"lng-french", description:"french"},
      {category:"language", tag:"lng-english", description:"english"},
      {category:"language", tag:"lng-arabic", description:"arabic"},
      {category:"language", tag:"lng-spanish", description:"spanish"},
      {category:"language", tag:"lng-unknown", description:"unkown"},

      {category:"utterance", tag:"utt-multi-lingual", description:"multilingual"},
      {category:"utterance", tag:"utt-multi-lingual-named-endity", description:"multilingual named entity"},
      {category:"utterance", tag:"utt-verbal-nod", description:"verbal nod"},

      {category:"speaker", tag:"spkr-single", description:"single"},
      {category:"speaker", tag:"spkr-multi", description:"multiple"},
      {category:"speaker", tag:"spkr-male", description:"male"},
      {category:"speaker", tag:"spkr-female", description:"female"},

      {category:"sound", tag:"ct-speech", description:"speech"},
      {category:"sound", tag:"ct-laughter", description:"laughter"},
      {category:"sound", tag:"ct-song", description:"song"},
      {category:"sound", tag:"ct-telephone", description:"telephone call"},
      {category:"sound", tag:"ct-bg-music", description:"background music"},
      {category:"sound", tag:"ct-fg-music", description:"foreground music"},
      {category:"sound", tag:"ct-tr-music", description:"transition music"},
      {category:"sound", tag:"ct-noise", description:"noise"},

      {category:"topic", tag:"ct-edu-covid", description:"Covid-19 education"},
      {category:"topic", tag:"ct-edu-islam", description:"islamic education"}
    ];

  }

  handleChange(e) {
    var tag = e.target.value;
    var selectedTags = this.state.selectedTags;

    if(e.target.checked){
      selectedTags.add(tag);
    }else{
      selectedTags.delete(tag);
    }

    this.setState({ value: e.target.value, selectedTags: selectedTags});
  }

  getRawMarkup() {
    return { __html: "You typed " + this.state.value };
  }

  getTagCategories() {
    return this.tags.map(t => t.category).filter((x, i, a) => a.indexOf(x)==i);
  }

  getTagsForCategory(category){
    return this.tags.filter(t => t.category == category).map(t => 
      <div key={t.tag}>
        <input id={t.tag} type='checkbox' value={t.tag} onClick={this.handleChange}></input>
        <label htmlFor={t.tag}>Contains {t.description} {t.category}</label>
      </div>
    );
  }

  render() {
    var categories = this.getTagCategories().map(c => 
      <div key={c} className='tagCategory'> 
        <div className='categoryTitle'>{c}</div> 
        {this.getTagsForCategory(c)} 
      </div>
    );

    
    return (
      <div className="TagEditor">
        <h1>Tags</h1>
        {categories}
        <h1>Audio Metadata</h1>
        <textarea className="composedTags" value={Array.from(this.state.selectedTags).sort().join("; ")} readOnly={true}>
        </textarea>
      </div>
    );
  }
}

ReactDOM.render(
  <TagEditor />,
  document.getElementById('tag-editor')
);