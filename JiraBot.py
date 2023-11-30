from atlassian import jira
import requests
import datetime



jira = jira.Jira(
    url = 'https://jira.abcdefgh.com/',
    username = '',
    password = ''
)
filterquery = ''
ct  = datetime.datetime.now()
timestamp = str(ct)[0:10]
timestamp2 = str(ct)[0:19]
outfilename = 'path_'+timestamp+'.csv'
#dashboard = '1234'


def getjiradata(JQL):
    start = 0
    jiraresponses = list()
    size = 50
    while True:
        data = jira.jql(JQL, fields='*all', start = start)
        jiraresponse = data.get('issues')
        start = start + (len(jiraresponse))
        if len(jiraresponse) == 0:
            break
        jiraresponses.append(jiraresponse)
    return jiraresponses

def printcounts(output):
    print('Total Issues: ',len(output))
    print('Status: Done, No. of Issues: ', sum([x.count('Done') for x in output]))
    print('Status: Ready For Delivery, No. of Issues: ', sum([x.count('Ready For Delivery') for x in output]))
    print('Status: Client Analysis, No. of Issues: ', sum([x.count('Client Analysis') for x in output]))
    print('Status: In Progress, No. of Issues: ', sum([x.count('In Progress') for x in output]))
    print('Status: Backlog, No. of Issues: ', sum([x.count('Backlog') for x in output]))
    print('Status: Delivered, No. of Issues: ', sum([x.count('Delivered') for x in output]))



def main():
    JQL = filterquery
    #db_id = dashboard
    jiraresponses = getjiradata(JQL)
    output = []
    for jiraresponse in jiraresponses:
        for issues in jiraresponse:
            fields = issues.get('fields')
            issue_key = issues.get('key')
            status = fields.get('status')
            status_code = status.get('name')
            summary = fields.get('summary').replace(',','')
            if summary == None:
                summary = ''
            try:
                assignee = fields.get('assignee')
                assignee_name = assignee.get('displayName')
            except:
                assignee_name = 'Unassigned'
            output.append([issue_key, summary, assignee_name, status_code])
    printcounts(output)
    with open(outfilename,'w') as outfile:
        outfile.write('Issue Key,'+'Summary,'+'Assignee,'+'Status' + '\n')
        for i in output:
            string = ','.join(i)
            outfile.write(string+'\n')





if __name__ == '__main__':
    try:
        main()
    except NameError as e:
        print('Name Error :', e)
    except requests.exceptions.HTTPError as e:
        print('HTTPError, contact programmer :', e)
    except AttributeError as e:
        print('Attribute Error :', e)






