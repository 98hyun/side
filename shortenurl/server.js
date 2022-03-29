const express=require('express')
const mongoose=require('mongoose')
const ShortUrls=require('./models/shorturl')
const app=express()

mongoose.connect('mongodb://localhost/urlshorten',{
    useNewUrlParser:true,useUnifiedTopology:true
})

app.set('view engine','ejs')
app.use(express.urlencoded({
    extended:false
}))

app.get('/',async function(req,res){
    const shorturls=await ShortUrls.find()

    res.render('index',{
        shorturls:shorturls,
    })
})

app.post('/shorturls', async function(req,res){
    if (ShortUrls.findOne(req.body.fullurl)){
        // ## delete
        // ShortUrls.deleteOne({
        //     fullurl:req.body.fullurl
        // }).then(function(){
        //     console.log("Data deleted"); // Success
        // }).catch(function(error){
        //     console.log(error); // Failure
        // });
        res.redirect('/')
    }
    else{
    await ShortUrls.create({
        full:req.body.fullurl
    })

    res.redirect('/')
    }
})

app.get('/:shorturl',async function(req,res){
    const shorturl=await ShortUrls.findOne({
        short:req.params.shorturl
    })

    if (shorturl==null){
        return res.sendStatus(404)
    }
    shorturl.clicks++
    shorturl.save()

    res.redirect(shorturl.full)
})

app.listen(process.env.PORT||5000);