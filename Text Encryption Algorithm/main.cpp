#include <iostream>
#include <cstring>
#include <windows.h>
#include <fstream>
#define _WIN32_WINNT 0x0500
#include <MMsystem.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <time.h>
void CaeEnc();
void viewfile(char u[100]);
void CaeDec();
int keygen();
void FCreate();
void mainmenu();
void calls();
int checkstat(char u[100]);
int checkreg(char u[100]);
void changestat(char u[100],int h);
void FENC();
void FEDIT();
void FDEC();
void ENCSTAT();
void err();
void registry(char u[100],int v,int y[50000],int siz,int ind);
int verify(char u[100],int v);
using namespace std;
char Yes[20]="ENCRYPTED",No[20]="NON-ENCRYPTED";
class X
{
    int ky;//Password
    int status;//1-Encrypted,0-Decrypted
public:
    X()
    {
        ky = -1;
    }
    char a[100];//Name
    int b[50000];//File script
    int sc;//Script count
    int retstat()
    {
        return this->status;
    }
    void setstat(int h)
    {
        this->status = h;
    }
    int retkey()
    {
        return this->ky;
    }
    void askey(int h)
    {
        this->ky=h;
    }
    void fordec(int d)
    {
        d = this->sc;
    }
    void bassign(int g[])
    {
        int i=0;
        while(i<this->sc)
        {
            g[i] = this->b[i];
            ++i;
        }
    }
}temp[2000];
int no=0;
int main()
{
    mainmenu();
    cin.sync();
    cout << "\n\nTerminating....\n\n";
    Sleep(100);
    return 0;
}
void mainmenu()
{
    char t,c;
    calls();
    cin.sync();
    do
    {
       system("cls");
       cin.sync();
       PlaySound(TEXT("Sound.wav"),NULL,SND_FILENAME|SND_ASYNC);
       cout << "WELCOME\n";
       Sleep(100);
       cout << "\n->Caesar Encryption(1)";
       Sleep(100);
       cout << "\n->Caesar Decryption(2)";
       Sleep(100);
       cout << "\n->File Creation(3)";
       Sleep(100);
       cout << "\n->File Encryption(4)";
       Sleep(100);
       cout << "\n->File Decryption(5)";
       Sleep(100);
       cout << "\n->File Editing(6)";
       Sleep(100);
       cout << "\n->Encryption Status(7)";
       Sleep(100);
       cout << "\n\nEnter Your Choice(1-7 or 'b' for return): ";
       Sleep(100);
       goto mn;
       mn:
       {
          cin >> c;
       }
       cin.sync();
       if(c!='1'&&c!='2'&&c!='3'&&c!='4'&&c!='5'&&c!='6'&&c!='7'&&c!='b')
       {
           cout << "\nEnter Again:\n";
           goto mn;
       }
       else if(c=='1')
       {
           calls();
           system("cls");
           CaeEnc();
       }
       else if(c=='2')
       {
           calls();
           system("cls");
           CaeDec();
       }
       else if(c=='3')
       {
           calls();
           system("cls");
           FCreate();
       }
       else if(c=='4')
       {
           calls();
           system("cls");
           FENC();
       }
       else if(c=='5')
       {
           calls();
           system("cls");
           FDEC();
       }
       else if(c=='6')
       {
           calls();
           system("cls");
           FEDIT();
       }
       else if(c=='7')
       {
           calls();
           system("cls");
           ENCSTAT();
       }
       else if(c=='b')
       {
           calls();
           system("cls");
           return;
       }
       cout << "\nWould you Like to enter the main menu?(Y/y): ";
       cin >> t;
       calls();
    }while(t=='Y'||t=='y');
    return;
}
void FCreate()
{
    cin.sync();
    char q[30],w[500],g;
    cout << "Enter File Name(Text/Note): ";
    gets(q);
    ofstream k(q,ios::out);
    if(k)
    {
        cout << "\n\tSUCCESSFULLY CREATED\n\n";
        calls();
    }
    else
    {
        cout << "\nOOPS OUT OF STORAGE... SORRY...\n";
        return;
    }
    cin.sync();
    do
    {
        cout << "\nEnter Information Required(no more than 500 at a time):\n";
        cin.sync();
        k.seekp(0,ios::end);
        cin.getline(w,500);
        k << w;
        cout << "\nWould you Like to enter more?(Y/y): ";
        cin.sync();
        cin >> g;
    }while(g=='y'||g=='Y');
    cout << "\nGreat Job!";
    for(int j=0;j<15;++j);
    return;
}
void FENC()
{
    cin.sync();
    char e[50],message,ch;
    char t;
    int f;
    int x[50000];
    int key;
    int dg;
    int in = 0;
    fstream k;
    goto frt;
    frt:
    {
        cout << "Enter File Name to Encrypt(Type 'GoBack' to return to main menu):\n ";
        gets(e);
        if(strcmpi(e,"GoBack")==0)
        {
            return;
        }
        k.open(e,ios::in|ios::out);
    }
    cin.sync();
    if(k)
    {
        cout << "SUCCESSFULLY ACCESSED";
        calls();
        if(checkreg(e)==1)
        {
            if(checkstat(e)==1)
            {
               cout << "\nFile Already Encrypted....Cannot Re-Encrypt....=(\n";
               return;
            }
            else if(checkstat(e)==0)
            {
                int c=6;
                goto lab;
                lab:
                {
                    --c;
                    cin.sync();
                    cout << "\nEnter Your Key to Re-Encrypt:(DO NOT SHARE): ";
                    cin >> dg;
                 }
                 int d = verify(e,dg);
                 if(d!=1)
                 {
                    for( ;c>0&&d!=1;)
                    {
                        err();
                        cout << "\nIncorrect Key... =( ... Enter Again(" << c << " tries left):\n";
                        goto lab;
                    }
                 }
                 if(c==0)
                 {
                    err();
                    cout << "\nSorry, File is unaccessible...";
                    return;
                 }
                 f = dg;
                 in++;
                 goto maingame;
            }
        }
    }
    else
    {
        cout << "\nNO SUCH FILE EXISTS. Enter Name Again: ";
        goto frt;
    }
    k.seekg(0);
    do
    {
        cin.sync();
        cout << "\nDo you Want to create a key(1)? or do you want a generated key(Safer)(2): ";
        cin >> t;
        if(t=='1')
        {
            calls();
            system("cls");
            cout << "\nEnter your key(4 digit pin only): ";
            cin >> f;
            break;
        }
        else if(t=='2')
        {
            calls();
            system("cls");
            f = keygen();
            cout << "\nYour Key(Do Not Share): " << f << endl << endl;
            system("pause");
            system("cls");
            break;
        }
        else
        {
            err();
            cout << "\nEnter again...\n";
        }
    }while(t!='1'||t!='2');
    cin.sync();
    maingame:
    {
    cout << "\nENCRYPTING....DO NOT TURN OFF THE COMPUTER...";
    PlaySound(TEXT("Sound.wav"),NULL,SND_FILENAME|SND_ASYNC);
    for(int d=0;d<50000;++d)
    {
        x[d]='\0';
    }
    int q=0,r;
    r = f;
    while(r!=0)
    {
        q = q + (r%10);
        r/=10;
    }
    if(q>9)
    {
        q = f%10;
    }
    int i=0,j=1;
    k.seekg(0,ios::end);
    int qw = k.tellg();
    k.seekg(0);
    while(i<qw)
    {
        if(j>2)
        {
            j=1;
        }
        int pos;
        pos = k.tellg();
        k.get(message);
        if(i%2==0)
        {
            if(isalnum(message))
            {
                if(isalpha(message))
                {
                    if(isupper(message))
                    {
                        x[i]=0;
                        message = char(int(message)+ (q*j));
                    }
                    else if(islower(message))
                    {
                        x[i]=1;
                        message = toupper(message);
                        message = char(int(message) + (q*j));
                   }
                }
                else if(isdigit(message))
                {
                    x[i]=2;
                    message = char(message+33);
                }
            }
            else
            {
                x[i]=3;
                message = char(int(message)+j);
            }

        }
        else if(i%2==1)
        {
            if(isalnum(message))
            {
                if(isupper(message))
                {
                    x[i] =0;
                    message = char(int(message) - q*j);
                }
                else if(islower(message))
                {
                    x[i] =1;
                    message = toupper(message);
                    message = char(int(message) - q*j);
                }
                else if(isdigit(message))
                {
                    x[i]=2;
                    message = char(message+33);
                }
            }
            else
            {
                x[i]=3;
                message = char(int(message)+j);
            }
        }
        k.seekp(pos);
        k << message;
        ++j;
        ++i;
    }
    calls();
    cout << "\nSUCCESSFULLY ENCRYPTED\n";
    cin.sync();
    registry(e,f,x,qw,in);
    k.close();
    }
    return;
}
void FEDIT()
{
    cin.sync();

    char e[50],message,ch;
    fstream k;
    int key,d;
    int c=6;
    X u;
    frt:
    {
        cout << "Enter File Name(NOTE:FILE EDITING IS POSSIBLE ONLY IF FILE IS DECRYPTED)(Type 'GoBack' to return to main menu):\n ";
        gets(e);
        if(strcmpi(e,"GoBack")==0)
        {
            return;
        }
        k.open(e,ios::in|ios::out);
    }
    if(k)
    {
        cout << "FILE SUCCESSFULLY FOUND";
        calls();
        if(checkreg(e)==1)
        {
            if(checkstat(e)==1)
            {
                cout << "\nFILE IS ENCRYPTED...Unable to Edit....Sorry...=(\n";
                return;
            }
        }
        if(checkreg(e)==1)
        {
            ifstream v("Private",ios::in|ios::binary);
            v.seekg(0,ios::beg);
            int flag=0;
            int dg;
            while(flag==0)
            {
                v.read((char*)&u,sizeof(X));
                if(strcmp(u.a,e)==0)
                {
                   flag=1;
                   int c=6;
                   goto lab;
                   lab:
                   {
                       --c;
                       cin.sync();
                       cout << "\nEnter Your Key to EDIT:(DO NOT SHARE): ";
                       cin >> dg;
                    }
                    int d = verify(e,dg);
                    if(d!=1)
                    {
                        for( ;c>0&&d!=1;)
                       {
                           err();
                           cout << "\nIncorrect Key... =( ... Enter Again(" << c << " tries left):\n";
                           goto lab;
                        }
                    }
                    if(c==0)
                    {
                       err();
                       cout << "\nSorry, File is unaccessible...";
                       return;
                    }
                }
            }
         }

    }
    else
    {
        cout << "\nNO SUCH FILE EXISTS. Enter Name Again.\n\n";
        goto frt;
    }
    calls();
    system("cls");
    cin.sync();
    cout << "\nWould You Like to Truncate File(Erase Complete Data)?(Y/y for yes,any other character for no): ";
    cin >> ch;
    calls();
    if(ch=='y'||ch=='Y')
    {
        k.close();
        k.open(e,ios::in|ios::out|ios::trunc);
    }
    system("cls");
    cin.sync();
    char w[500],g;
    if(ch=='y'||ch=='Y')
    {
        do
        {
            cout << "\nEnter Data to Add(max 500 at a time):\n";
            cin.sync();
            k.seekp(0,ios::end);
            cin.getline(w,500);
            k << w;
            cout << "\nWould you Like to enter more?(Y/y for yes,any other character for no): ";
            cin.sync();
            cin >> g;
         }while(g=='y'||g=='Y');
    }
    else
    {
        cout << "Current File Contents:\n";
        viewfile(e);
        cin.sync();
        do
        {
            cout << "\nEnter Data to Add(Enter 'GoBack'(Case Sensitive)to finish adding)(max 500 at a time):\n";
            cin.sync();
            k.seekp(0,ios::end);
            cin.getline(w,500);
            k << w;
            cout << "\nWould you Like to enter more?(Y/y for yes,any other character for no): ";
            cin.sync();
            cin >> g;
         }while(g=='y'||g=='Y');
    }
    return;
}
void FDEC()
{
    cin.sync();
    char e[50],message,ch;
    fstream k;
    int key,d,x2[50000];
    int c=6;
    X u;
    frt:
    {
        cout << "Enter File Name to Decrypt(Type 'GoBack' to return to main menu):\n ";
        gets(e);
        if(strcmpi(e,"GoBack")==0)
        {
            return;
        }
        k.open(e,ios::in|ios::out);
    }
    if(k)
    {
        cout << "FILE SUCCESSFULLY FOUND";
        calls();
        if(checkreg(e)==1)
        {
            if(checkstat(e)==0)
            {
                cout << "\nFile Already Decrypted....Cannot Re-Decrypt....=(\n";
                return;
            }
            else if(checkstat(e)==1)
            {
                ifstream v("Private",ios::in|ios::binary);
                v.seekg(0,ios::beg);
                int flag=0;
                while(flag==0)
                {
                    v.read((char*)&u,sizeof(X));
                    if(strcmp(u.a,e)==0)
                    {
                       flag=1;
                       u.bassign(x2);
                    }
                }
                goto lab;
            }
        }
        if(checkreg(e)==0)
        {
            cout << "\nFile Not Encrypted & Registered!!! Encryption and Registering Required...=(\n";
            return;
        }
        ifstream v("Private",ios::in|ios::binary);
        v.seekg(0,ios::beg);
        int flag=0;
        while(flag==0)
        {
            v.read((char*)&u,sizeof(X));
            if(strcmp(u.a,e)==0)
            {
                flag=1;
                u.bassign(x2);
            }
        }
    }
    else
    {
        cout << "\nNO SUCH FILE EXISTS. Enter Name Again.\n\n";
        goto frt;
    }
    k.seekg(0);
    lab:
    {
        --c;
        cout << "\nEnter Key(Do Not Share): ";
        cin >> key;
    }
    d = verify(e,key);
    if(d!=1)
    {
        for( ;c>0&&d!=1;)
        {
            err();
            cout << "\nIncorrect Key... =( ... Enter Again(" << c << " tries left):\n";
            goto lab;
        }
    }
    if(c==0)
    {
        err();
        cout << "\nSorry, File is unaccessible...";
        return;
    }
    cout << "\nFILE ACCESSED SUCCESSFULLY\n";
    cin.sync();
    cout << "\nDECRYPTING....DO NOT TURN OFF THE COMPUTER...";
    PlaySound(TEXT("Sound.wav"),NULL,SND_FILENAME|SND_ASYNC);
    int q=0,r;
    r = key;
    while(r!=0)
    {
        q = q + (r%10);
        r/=10;
    }
    if(q>9)
    {
        q = key%10;
    }
    int i=0,j=1;
    k.seekg(0,ios::end);
    int qw = k.tellg();
    k.seekg(0);
    while(i<qw)
    {
        int pos;
        pos = k.tellg();
        k.get(message);
        if(j>2)
        {
            j=1;
        }
        if(i%2==0)
        {
            if(x2[i]==0)
            {
                message = char(int(message)-(q*j));
            }
            else if(x2[i]==1)
            {
                message = tolower(message);
                message = char(int(message)-(q*j));
                message = tolower(message);
            }
            else if(x2[i]==2)
            {
                message = char(message-33);
            }
            else if(x2[i]==3)
            {
                message = char(int(message)-j);
            }
        }
        else if(i%2==1)
        {
            if(x2[i]==0)
            {
                message = char(int(message)+(q*j));
            }
            else if(x2[i]==1)
            {
                message = tolower(message);
                message = char(int(message)+(q*j));
                message = tolower(message);
            }
            else if(x2[i]==2)
            {
                message = char(message-33);
            }
            else if(x2[i]==3)
            {
                message = char(int(message)-j);
            }
        }
        k.seekp(pos);
        k << message;
        ++i;
        ++j;
    }
    calls();
    cout << "\nSUCCESSFULLY DECRYPTED\n";
    k.close();
    changestat(e,0);
    system("pause");
    system("cls");
    cout << "\nWould you like to see the contents?(Y/y): ";
    cin.sync();
    char z;
    cin >> z;
    if(z=='Y'||z=='y')
    {
        viewfile(e);
    }
    else
        cout << "\nThank You =)";
    cout << endl;
    return;
}
void CaeEnc()
{
    cin.sync();
    char message[100], ch;
    int i,key;
    cout << "Enter a message to encrypt: ";
    cin.getline(message, 100);
    cin.sync();
    cout << "Enter key: ";
    cin >> key;
    int q=0,r;
    r = key;
    while(r!=0)
    {
        q = q + (r%10);
        r/=10;
    }
    if(q>9)
    {
        q = key%10;
    }
    key = q;
    cin.sync();
    for(i = 0; message[i] != '\0'; ++i)
    {
        ch = message[i];
        if(ch >= 'a' && ch <= 'z')
        {
            ch = ch + key;
            if(ch > 'z')
            {
                ch = ch - 'z' + 'a' - 1;
            }
            message[i] = ch;
        }
        else if(ch >= 'A' && ch <= 'Z')
        {
            ch = ch + key;
            if(ch > 'Z')
            {
                ch = ch - 'Z' + 'A' - 1;
            }
            message[i] = ch;
        }
    }
    cout << "Encrypted message: " << message;
    return;
}
void CaeDec()
{
    cin.sync();
    char ms[100], ch;
    int i, key;
    cout << "Enter a message to decrypt: ";
    cin.getline(ms,100);
    cin.sync();
    cout << "Enter key: ";
    cin >> key;
    int q=0,r;
    r = key;
    while(r!=0)
    {
        q = q + (r%10);
        r/=10;
    }
    if(q>9)
    {
        q = key%10;
    }
    key = q;
    cin.sync();
    for(i = 0;ms[i]!='\0';++i)
    {
        ch = ms[i];
        if(ch >= 'a' && ch <= 'z')
        {
            ch = ch - key;
            if(ch < 'a')
            {
                ch = ch + 'z' - 'a' + 1;
            }
            ms[i] = ch;
        }
        else if(ch >= 'A' && ch <= 'Z')
        {
            ch = ch - key;
            if(ch < 'A')
            {
                ch = ch + 'Z' - 'A' + 1;
            }
            ms[i] = ch;
        }
    }
    cout << "Decrypted message: " << ms;
    return;
}
void calls()
{
    PlaySound(TEXT("Bleep.wav"),NULL,SND_FILENAME|SND_ASYNC);
    Sleep(1600);
    return;
}
void registry(char u[100],int v,int y[50000],int siz,int ind)
{
    cout << "\nRegistering File...";
    ofstream k("Private",ios::out|ios::ate|ios::app|ios::binary);
    strcpy(temp[no].a,u);
    temp[no].askey(v);
    temp[no].sc=siz;
    for(int c=0;c<siz;++c)
    {
        temp[no].b[c] = y[c];
    }
    temp[no].setstat(1);
    if(ind==1)
    {
        fstream ik("Private",ios::in|ios::out|ios::binary);
        ik.seekg(0,ios::beg);
        X jk;
        int flag=0;
        while(flag==0)
        {
           int pos = ik.tellg();
           ik.read((char*)&jk,sizeof(X));
           if(strcmp(jk.a,u)==0)
           {
               flag=1;
               ik.seekg(pos);
               ik.write((char*)&temp[no],sizeof(X));
               ik.close();
               cout << "\nSUCCESSFULLY REGISTERED...";
               calls();
               system("pause");
               return;
           }
        }
    }
    k.write((char*)&temp[no],sizeof(X));
    k.close();
    ofstream m("List",ios::out|ios::app|ios::ate);
    m << u << "\n";
    m.close();
    cout << "\nSUCCESSFULLY REGISTERED...";
    calls();
    system("pause");
    return;
    ++::no;
}
void err()
{
    PlaySound(TEXT("Err.wav"),NULL,SND_FILENAME|SND_ASYNC);
    Sleep(1200);
    return;
}
int verify(char u[100],int v)
{
    ifstream y("Private",ios::in|ios::binary);
    y.seekg(0,ios::beg);
    X tem;
    while(!y.eof())
    {
        y.read((char*)&tem,sizeof(X));
        if(strcmp(tem.a,u)==0)
        {
            if(tem.retkey()==v)
            {
                y.close();
                return 1;
            }
            else
            {
                y.close();
                return 0;
            }
        }
    }
}
void viewfile(char u[100])
{
    system("cls");
    ifstream k(u,ios::in);
    char q;
    k.seekg(0,ios::end);
    int qw = k.tellg();
    int i=0;
    k.seekg(0);
    while(i<qw)
    {
        k.get(q);
        cout << q;
        ++i;
    }
    k.close();
    return;
}
int keygen()
{
    int a;
    srand(time(NULL));
    a = rand() %9999 + 999;
    return a;
}
int checkstat(char u[100])
{
    ifstream y("Private",ios::in|ios::binary);
    y.seekg(0,ios::beg);
    X tem;
    while(!y.eof())
    {
        y.read((char*)&tem,sizeof(X));
        if(strcmp(tem.a,u)==0)
        {
            if(tem.retstat()==1)
                return 1;
            else
                return 0;
        }
    }
}
void changestat(char u[100],int h)
{
    fstream y("Private",ios::in|ios::out|ios::binary);
    y.seekg(0,ios::beg);
    X tem;
    while(!y.eof())
    {
        int t = y.tellg();
        y.read((char*)&tem,sizeof(X));
        if(strcmp(tem.a,u)==0)
        {
            tem.setstat(h);
            y.seekg(t);
            y.write((char*)&tem,sizeof(X));
            return;
        }
    }
}
int checkreg(char u[100])
{
    ifstream y("List",ios::in);
    y.seekg(0,ios::beg);
    char t[100];
    y.seekg(0,ios::end);
    int pos = y.tellg();
    if(pos==-1)
    {
        return 0;
    }
    y.seekg(0);
    while(!y.eof())
    {
        int kr;
        y.getline(t,100,'\n');
        if(strcmp(t,u)==0)
        {
            return 1;
        }
    }
    return 0;
}
void ENCSTAT()
{
    cin.sync();
    char e[50],ch;
    fstream k;
    int key,d,x2[50000];
    int c=6;
    X u;
    frt:
    {
        cout << "Enter File Name to CHECK(Type 'GoBack' to return to main menu):\n ";
        gets(e);
        if(strcmpi(e,"GoBack")==0)
        {
            return;
        }
        k.open(e,ios::in|ios::out);
    }
    if(k)
    {
        cout << "FILE SUCCESSFULLY FOUND";
        calls();
        system("cls");
        if(checkreg(e)==1)
        {
            if(checkstat(e)==1)//enc
            {
                for(int i=0;i<20;++i)
                {
                    Sleep(10);
                    cout << "-*";
                }
                cout << "\n\n\t";
                for(int i=0;i<20;++i)
                {
                    cout << Yes[i];
                    Sleep(10);
                }
                cout << "\t=)\n\n";
                for(int i=0;i<20;++i)
                {
                    Sleep(10);
                    cout << "-*";
                }
                cout << "\n";

            }
            else if(checkstat(e)==0)//dec
            {
                for(int i=0;i<20;++i)
                {
                    Sleep(10);
                    cout << "-*";
                }
                cout << "\n\n\t";
                for(int i=0;i<20;++i)
                {
                    cout << No[i];
                    Sleep(10);
                }
                cout << "\t=(\n\n";
                for(int i=0;i<20;++i)
                {
                    Sleep(10);
                    cout << "-*";
                }
                cout << "\n";
            }
        }
        else if(checkreg(e)==0)
        {
            err();
            cout << "\nFile Not Encrypted & Registered!!! Encryption and Registering Required...=(\n";
            return;
        }
        return;
    }
    else
    {
        cout << "\nNO SUCH FILE EXISTS. Enter Name Again.\n\n";
        goto frt;
    }
}
