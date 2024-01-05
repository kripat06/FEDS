//
//  ContentView.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/9/23.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationStack {
            VStack {
                Spacer().frame(height: 50)
                Image("feds-logo-1")
                    .resizable()
                    .frame(width: 750, height: 620)
                NavigationLink(destination: ParkListView()) {
                    RoundedRectangle(cornerRadius: 16)
                        .strokeBorder(Color.orange , lineWidth: 4)
                        .background(RoundedRectangle(cornerRadius: 16).fill(Color.gray))
                        .frame(width: 225, height: 75)
                        .overlay {
                            Text("View Parks")
                                .font(.system(size: 35))
                                .bold()
                                .foregroundColor(Color.yellow)
                                .padding()
                        }
                }
                Spacer()
            }
            .background(Color.white)

//            AsyncImage(url: URL(string: "https://feds-app-assets.s3.us-west-2.amazonaws.com/static/start_screen.jpeg")) { image in image
//                    .resizable()
//                    .scaledToFit()
//                    .aspectRatio(contentMode: .fill)
//                    .overlay(
//                        VStack {
//                            Spacer().frame(height: 50)
//                            Image("feds-logo-1")
//                                .resizable()
//                                .frame(width: 750, height: 620)
//                            NavigationLink(destination: ParkListView()) {
//                                RoundedRectangle(cornerRadius: 16)
//                                    .strokeBorder(Color.orange , lineWidth: 4)
//                                    .background(RoundedRectangle(cornerRadius: 16).fill(Color.gray))
//                                    .frame(width: 225, height: 75)
//                                    .overlay {
//                                        Text("View Parks")
//                                            .font(.system(size: 35))
//                                            .bold()
//                                            .foregroundColor(Color.yellow)
//                                            .padding()
//                                    }
//                            }
//                            Spacer()
//                        }
//                    )
//            } placeholder: {
//              Image(systemName: "photo")
//                    .resizable()
//                    .scaledToFit()
//                    .frame(width: 100, height: 100, alignment: .center)
//                    .foregroundColor(.white.opacity(0.7))
//                    .frame(maxWidth: .infinity, maxHeight: .infinity)
//            }
//            .frame(width: .infinity, height: .infinity)
////            .padding(0)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
