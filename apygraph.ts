import { BaseCommandInteraction, Client } from "discord.js";
import { ICommand } from "./ICommand";
import dotenv from 'dotenv';
import fetch from 'cross-fetch';
import { ApolloClient,InMemoryCache, HttpLink, gql } from '@apollo/client';
import { networkMetadata, supportedChainIds } from '@0xnodes/shared/networks';

dotenv.config();

export const Apr: ICommand = {
    name: "apr",
    description: "list all current APR's from all chains",
    type: "CHAT_INPUT",
    run: async (client: Client, interaction: BaseCommandInteraction) => {

        const gqlClient = new ApolloClient({
            link: new HttpLink({uri: process.env.APOLLO_URL, fetch}),
            cache: new InMemoryCache()
          });

        // query
        const query = gql`
            query GetStrategies($chainId: Int!) {
                strategies(chainId: $chainId) {
                    chainId
                    name
                    apy
                    description
            }
        }`

        const header = (chain: any) => `${chain.chainName}:`
        const row = (strategy: any) => `${strategy.name} ${strategy.apy}`
        var output: string[] = []

        await Promise.all(supportedChainIds.map(async (chainId) => {
                
            const result = await gqlClient.query({
                query,
                context: {
                    chainId,
                },
                variables: {
                    chainId,
                },
            })

            output.push(header(networkMetadata[chainId]));

            result.data.strategies.forEach((strategy: any) => {
                if (strategy.apy !== 0)
                    output.push(row(strategy));
            })
        }))

        const content = output.join("\n")

        await interaction.followUp({
            ephemeral: true,
            content
        })
    }
}