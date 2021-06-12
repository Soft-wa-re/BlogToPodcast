---
layout: post
title:  "Read The Error Message"
tags: [Programing, GeneralAdvice, Always]
permalink: /read-the-error-message/
---
 
See: [Learn to Read the Source, Luke](https://blog.codinghorror.com/learn-to-read-the-source-luke/)
 
I just want to throw this out there because this tripped me up recently.  So maybe if I write a blag post, I won't do it again.
 
So, right now I am in between teams, about to leave one, and getting on-boarded with a new one, and my time is a little crunched.  There is an important issue I need to finish up to leave my last team in a good state, so I needed to get it done soon before I don't have any more time to do it. 
 
The command that was failing was `yarn install` on the build server.  It was complaining `there seems to be a problem with your internet connection`. Ok well our internal network/vpn has always been quite ficky about the domains it will and won't connect to, this is nothing new.  I don't like it but I guess the best pragmatic solution will be to cache the `node_modules` in the repo.  So I started hacking up a quick node.js script to remove `node_modules` from the `.gitignore`, update the `node_modules`, restore the `.gitignore`.  Ok that didn't work. So I moved on to another solution, that then didn't work, then another.
 
Fast Forward to me reading through the build log for what felt like the 20th time, and then I see it.  An error message complaining blahblahblah I can't `yarn install` package from `repo.internaldomain.com/artifactory`  Oh right we never have been able to get to that server from our side of the company network, and I could have read that error message at the beginning if I wasn't in such a hurry, and quick to jump to conclusions.
 
So I think the moral of the story here is to `measure twice, and cut once`.
 
One more note I want to get in here.  If you made it this far you might have questions about shortcuts. That's fine.  So the project I was leaving was getting shut down, and the project I was going to was getting spun up. Naturally.  This `yarn install` package that was being added to the build server, was actually the source code, and dependencies from the new project.  That's kinda why I was getting pulled onto the new project.  Even though our old project was getting shut down, what I did to gain experience, for me and my team was to bring the new project to us so we could contribute to it sooner rather than later.  Unfortunately just as we were starting to hit our stride deleting the old source code, and importing the new source code, I got pulled off the project.  But to leave the old team in a good state one of the last things I made sure we had working was build server.  So yeah, there were shortcuts here we were not proud of, but that's the wrong thing to focus on.  What was awesome was, even though we got stuck maintaining some old clunky software, we brought the new stuff to us, learned it ourselves, and started contributing to it, before they could even shut down the old project.  This whole story is worth it's own blog post, because there are some good lessons here in how to rock the boat, but I am going to take this pragmatic shortcut for now, and knock this blog post out in one hour.