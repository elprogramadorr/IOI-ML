#include <bits/stdc++.h>
#define pb push_back
#define vi vector<int>
#define int long long
using namespace std;

int res=0;
const int tam=2e5+5;
int dp[tam];
vector<vi>G;
void dfs(int nodo, int ant){
    dp[nodo]=G[nodo].size();
    res=max(res,dp[nodo]);
    int mayor=-1,segundo=-1;
    for(auto it : G[nodo]){
        if(it==ant)continue;
        dfs(it,nodo);
        int ayuda=dp[it]-1+G[nodo].size()-1;
        dp[nodo]=max(dp[nodo],ayuda);
        res=max(res,ayuda);
        if(dp[it]>mayor){
            segundo=mayor;
            mayor=dp[it];
        }else if(dp[it]>segundo){
            segundo=dp[it];
        }
    }

    if(segundo!=-1){
        int aux=mayor-1+segundo-1+G[nodo].size()-2;
        res=max(res,aux);
    }   
}

signed main(){
    ios_base::sync_with_stdio(0); cin.tie(0);
    int t,n,a,b;
    cin>>t;
    while(t--){
        cin>>n;
        G.assign(n+1,vi());
        for(int i=1;i<n;i++){
            cin>>a>>b;
            G[a].pb(b);
            G[b].pb(a);
        }
        res=1;
        dfs(1,-1);
        cout<<res<<"\n";
    }

    return 0;
}