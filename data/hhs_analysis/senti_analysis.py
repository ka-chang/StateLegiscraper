import matplotlib.pyplot as plt

### The input is the filter value got from the sentences filtering notebook
def senti_analysis(filter):
    filter_sen=[]
    months=[]
    for i in filter.keys():
        months.append(i.month)
        filter_sen.append({'text':filter[i], 'metadata':i.month})
    months=set(months)
    filter_m={}
    for i in months:
        filter_m[i]=[]
    for i in filter_sen:
        for j in months:
            if i['metadata']==j:
                filter_m[j].append(i['text']) ### get the dictionary of covid related sentences group by month
    for i in filter_m.keys():
        filter_m[i]=sum(filter_m[i], [])    #### erase the square brackets of the dictionary value
    from textblob import TextBlob
    blob={}
    for i in filter_m.keys():
        blob[i] = TextBlob(' '.join(filter_m[i]))
    listsen_cov_pol={}
    listsen_cov_sen={}
    for i in blob.keys():
        polarity=1
        for j in range(len(blob[i].sentences)):
            if blob[i].sentences[j].sentiment.polarity<polarity:
                polarity=blob[i].sentences[j].sentiment.polarity
                sentence=blob[i].sentences[j]
        listsen_cov_pol[i]=polarity
        listsen_cov_sen[i]=sentence
    listsen_cov_polp={}
    listsen_cov_senp={}
    for i in blob.keys():
        polarity=-1
        for j in range(len(blob[i].sentences)):
            if blob[i].sentences[j].sentiment.polarity>polarity:
                polarity=blob[i].sentences[j].sentiment.polarity
                sentence=blob[i].sentences[j]
        listsen_cov_polp[i]=polarity
        listsen_cov_senp[i]=sentence
    covsen={}
    for i in blob.keys():
        covsen[i]=blob[i].sentiment.polarity
    covlistsen = listsen_cov_pol.items()
    covlistsen = sorted(covlistsen)
    x3,y3 = zip(*covlistsen)
    covlistsenp = listsen_cov_polp.items()
    covlistsenp = sorted(covlistsenp)
    x4,y4 = zip(*covlistsenp)
    covsensen = covsen.items()
    covsensen = sorted(covsensen)
    x5,y5 = zip(*covsensen)
    plt.plot(x3,y3)
    plt.plot(x4,y4)
    plt.plot(x5,y5)
    plt.legend(['Lowest', 'Highest', 'Ave']) #label the line
    plt.show()
    print('The lowest scores are got by the following sentences:\n',listsen_cov_sen)
    print('The highest scores are got by the following sentences:\n',listsen_cov_senp)
