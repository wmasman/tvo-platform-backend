# Directus Data Requirements Checklist

## Overview

This document provides a comprehensive checklist of all data that the frontend application needs from Directus, organized by entity type, usage context, and required format. Use this checklist to ensure complete API coverage during the integration process.

---

## **Articles Data Requirements**

### **Core Article Fields**
- [ ] **id** (string) - Unique identifier
- [ ] **title** (string) - Article title
- [ ] **summaryCard** (string) - Short summary for cards
- [ ] **summaryDetail** (string, optional) - Detailed summary for article page
- [ ] **mainContent** (HTML string) - Full article content
- [ ] **smallImageUrl** (string, optional) - Thumbnail image
- [ ] **publication_date** (ISO string) - Publication date
- [ ] **estimated_reading_time** (number) - Reading time in minutes

### **Article Metadata**
- [ ] **isNew** (boolean) - Recently published flag
- [ ] **progressPercent** (number) - User reading progress (0-100)
- [ ] **relevanceScore** (number, optional) - For sorting/ranking
- [ ] **spotlight** (boolean, optional) - Featured content flag

### **Article Relationships**
- [ ] **extracted_authors** (AuthorPreview[]) - Article authors
  - [ ] id, name, avatarUrl, bioCard, articlesCount
- [ ] **concepts** (ConceptPreview[]) - Related concepts
  - [ ] id, name, descriptionCard, relatedArticlesCount
- [ ] **references** (Reference[], optional) - External references
  - [ ] text, url

### **Article Interactive Elements**
- [ ] **conceptsInteractive** (InteractiveConceptInArticle[]) - For concept highlighting
  - [ ] conceptId, conceptName, conceptDefinitionCard
  - [ ] sensesInArticle with evidenceSegments
- [ ] **sentences** (Sentence[], optional) - For text analysis
  - [ ] sentenceId, text, startOffset, endOffset

### **Article Related Content**
- [ ] **relatedArticlesPreview** (ArticlePreview[], optional) - Related articles
- [ ] **relatedInsightsPreview** (InsightPreview[], optional) - Related insights
- [ ] **relatedConceptsPreview** (ConceptPreview[], optional) - Related concepts
- [ ] **relatedAuthorsPreview** (AuthorPreview[], optional) - Related authors

### **User-Specific Article Data**
- [ ] **isSavedToLibrary** (boolean) - User saved status
- [ ] **progressPercent** (number) - User reading progress

### **Usage Context**
- **Article List Page**: Core fields + metadata + relationships (authors, concepts)
- **Article Detail Page**: All fields including interactive elements and related content
- **Article Cards**: ArticlePreview subset (id, title, summaryCard, smallImageUrl, publication_date, extracted_authors, isNew, progressPercent, isSavedToLibrary, estimated_reading_time)
- **Home Page Aggregations**: Core fields + relevanceScore + spotlight flag

---

## **Authors Data Requirements**

### **Core Author Fields**
- [ ] **id** (string) - Unique identifier
- [ ] **name** (string) - Author name
- [ ] **avatarUrl** (string, optional) - Profile picture
- [ ] **profileImageUrl** (string, optional) - Larger profile image
- [ ] **bioCard** (string) - Short bio for cards
- [ ] **bioDetail** (string, optional) - Full biography

### **Author Professional Info**
- [ ] **contactInfo** (object, optional)
  - [ ] email, website, phone, companyName
- [ ] **companyLogoUrl** (string, optional) - Company logo
- [ ] **authorStatus** (string, optional) - Status level
  - Values: 'new', 'inactive', 'Editor', 'Advisory Board', 'Bronze', 'Silver', 'Gold'
- [ ] **affiliation** (string, optional) - Organization affiliation
- [ ] **contributions** (number, optional) - Contribution count

### **Author Statistics**
- [ ] **articlesCount** (number) - Number of articles authored
- [ ] **relevanceScore** (number, optional) - For sorting/ranking

### **Author Relationships**
- [ ] **articlesAuthoredPreview** (ArticlePreview[], optional) - Authored articles
- [ ] **insightsContributedPreview** (InsightPreview[], optional) - Contributed insights
- [ ] **conceptsAssociatedPreview** (ConceptPreview[], optional) - Associated concepts
- [ ] **relatedAuthorsPreview** (AuthorPreview[], optional) - Related authors

### **Author Social & Contact**
- [ ] **socialLinks** (SocialLink[], optional) - Social media links
  - [ ] platform, url, icon

### **User-Specific Author Data**
- [ ] **isFollowedByUser** (boolean) - User follow status
- [ ] **isCurrentUserThisAuthor** (boolean) - Is this the current user
- [ ] **isNew** (boolean) - Recently added author flag

### **Usage Context**
- **Author Detail Pages**: All fields including relationships and social links
- **Author Cards**: AuthorPreview subset (id, name, avatarUrl, bioCard, authorStatus, articlesCount, isNew, isFollowedByUser)
- **Article Author Attribution**: Basic info (id, name, avatarUrl, bioCard)
- **Author Following**: User relationship data

---

## **Concepts Data Requirements**

### **Core Concept Fields**
- [ ] **id** (string) - Unique identifier
- [ ] **name** (string) - Concept name
- [ ] **descriptionCard** (string) - Short description for cards
- [ ] **definitionDetail** (string) - Full definition

### **Concept Metadata**
- [ ] **conceptStatus** (string) - Concept lifecycle status
  - Values: 'Generated', 'Published', 'Archived', 'Superseded', 'Deprecated'
- [ ] **metadata** (object) - Additional metadata
  - [ ] creationDate, lastUpdatedDate, version, domain, subDomain, tags

### **Concept Statistics**
- [ ] **relatedArticlesCount** (number) - Related articles count
- [ ] **relatedInsightsCount** (number) - Related insights count
- [ ] **relevanceScore** (number, optional) - For sorting/ranking
- [ ] **spotlight** (boolean, optional) - Featured concept flag

### **Concept Generation Info**
- [ ] **generatedBy** (Reference[], optional) - Sources that generated this concept
  - [ ] id, name, detailPageUrl

### **Concept Relationships**
- [ ] **relatedArticlesPreview** (ArticlePreview[], optional) - Related articles
- [ ] **relatedInsightsPreview** (InsightPreview[], optional) - Related insights
- [ ] **relatedConceptsPreview** (ConceptPreview[], optional) - Related concepts
- [ ] **relatedAuthorsPreview** (AuthorPreview[], optional) - Related authors

### **Concept Lifecycle Management**
- [ ] **supersededByConcept** (Reference, optional) - Replacement concept
- [ ] **deprecatesConcepts** (Reference[], optional) - Concepts this replaces

### **Concept Semantic Data**
- [ ] **senses** (Sense[], optional) - Different meanings/contexts
  - [ ] senseId, definition, examples, domain
- [ ] **sensesGroupedByArticle** (SensesInArticleGroup[], optional) - Grouped by source

### **User-Specific Concept Data**
- [ ] **isNew** (boolean) - Recently added concept flag
- [ ] **isSavedToLibrary** (boolean, optional) - User saved status
- [ ] **isFollowedByUser** (boolean, optional) - User follow status

### **Usage Context**
- **Concept List Page**: Core fields + statistics + user data
- **Concept Detail Page**: All fields including relationships and semantic data
- **Concept Cards**: ConceptPreview subset (id, name, descriptionCard, relatedArticlesCount, relatedInsightsCount, isNew, conceptStatus)
- **Article Concept Tags**: Basic info (id, name, descriptionCard)
- **Concept Network Visualization**: Relationships + status information

---

## **Insights Data Requirements**

### **Core Insight Fields**
- [ ] **id** (string) - Unique identifier
- [ ] **title** (string) - Insight title
- [ ] **summaryCard** (string) - Short summary for cards
- [ ] **summaryDetail** (string, optional) - Detailed summary
- [ ] **narrative_output** (HTML string) - Full insight content
- [ ] **smallImageUrl** (string, optional) - Thumbnail image

### **Insight Metadata**
- [ ] **creationDate** (ISO string) - Creation date
- [ ] **lastUpdatedDate** (ISO string, optional) - Last update
- [ ] **version** (string, optional) - Version number
- [ ] **insightStatus** (string, optional) - Lifecycle status
  - Values: 'Generated', 'Published', 'Archived', 'Superseded', 'Deprecated'

### **Insight Generation Info**
- [ ] **generatedBy** (Reference[], optional) - Sources that generated this insight
  - [ ] id, name, detailPageUrl

### **Insight Statistics**
- [ ] **related_article_count** (number) - Related articles count
- [ ] **related_authors_count** (number) - Related authors count
- [ ] **relevanceScore** (number, optional) - For sorting/ranking
- [ ] **spotlight** (boolean, optional) - Featured insight flag

### **Insight Relationships**
- [ ] **contributing_articlesPreview** (ArticlePreview[], optional) - Source articles
- [ ] **key_conceptsPreview** (ConceptPreview[], optional) - Key concepts
- [ ] **relatedArticlesPreview** (ArticlePreview[], optional) - Related articles
- [ ] **relatedInsightsPreview** (InsightPreview[], optional) - Related insights
- [ ] **relatedConceptsPreview** (ConceptPreview[], optional) - Related concepts
- [ ] **relatedAuthorsPreview** (AuthorPreview[], optional) - Related authors

### **Insight Lifecycle Management**
- [ ] **supersededByInsight** (Reference, optional) - Replacement insight
- [ ] **deprecatesInsights** (Reference[], optional) - Insights this replaces

### **Insight Engagement**
- [ ] **reactionCount** (object, optional) - User reactions
  - [ ] likes, dislikes, [custom reactions]
- [ ] **commentsData** (object, optional) - Comments system
  - [ ] totalComments, comments[], canCurrentUserComment, hasMoreComments

### **User-Specific Insight Data**
- [ ] **isNew** (boolean) - Recently created flag
- [ ] **isFollowedByUser** (boolean) - User follow status
- [ ] **isSavedToLibrary** (boolean) - User saved status

### **Usage Context**
- **Insight List Page**: Core fields + statistics + user data
- **Insight Detail Page**: All fields including relationships and engagement
- **Insight Cards**: InsightPreview subset (id, title, summaryCard, smallImageUrl, creationDate, related_article_count, key_conceptsPreview, reactionCount, isNew, isFollowedByUser, isSavedToLibrary, insightStatus)
- **Related Content**: Preview relationships

---

## **Thematic Collections Data Requirements**

### **Core Collection Fields**
- [ ] **id** (string) - Unique identifier
- [ ] **title** (string) - Collection title
- [ ] **descriptionCard** (string) - Short description for cards
- [ ] **descriptionDetail** (string, optional) - Full description
- [ ] **smallImageUrl** (string, optional) - Collection thumbnail
- [ ] **publication_date** (ISO string) - Publication date

### **Collection Editorial Info**
- [ ] **editors** (Editor[]) - Collection editors
  - [ ] id, name, avatarUrl

### **Collection Content**
- [ ] **items** (ThematicCollectionItemPreview[]) - Collection items
  - Union type: ArticlePreview | InsightPreview | ConceptPreview | AuthorPreview
  - [ ] itemType field to distinguish types

### **Collection Statistics**
- [ ] **relatedConceptsCount** (number) - Related concepts count
- [ ] **relatedArticlesCount** (number) - Related articles count
- [ ] **relatedInsightsCount** (number) - Related insights count

### **Collection Progress Tracking**
- [ ] **userProgress** (object, optional) - User progress
  - [ ] completedItems, totalItems
- [ ] **progressPercent** (number) - Progress percentage
- [ ] **authorsFeaturedPreview** (AuthorPreview[], optional) - Featured authors

### **User-Specific Collection Data**
- [ ] **isNew** (boolean) - Recently created flag
- [ ] **isFollowedByUser** (boolean, optional) - User follow status
- [ ] **isSavedToLibrary** (boolean, optional) - User saved status

### **Usage Context**
- **Thematic Collection Detail Page**: All fields including items and progress
- **Collection Cards**: ThematicCollectionPreview subset (id, title, descriptionCard, smallImageUrl, publication_date, editors, progressPercent, isNew, isFollowedByUser, isSavedToLibrary)
- **Collection Progress Tracking**: User progress data

---

## **User & Authentication Data Requirements**

### **Core User Fields**
- [ ] **id** (string) - Unique identifier
- [ ] **name** (string, optional) - Display name
- [ ] **email** (string, optional) - Email address
- [ ] **avatarUrl** (string, optional) - Profile picture
- [ ] **isLoggedIn** (boolean) - Authentication status

### **User Profile Data**
- [ ] **shortBio** (string, optional) - Brief biography
- [ ] **interests** (string[], optional) - User interests
- [ ] **domains** (string[], optional) - Professional domains
- [ ] **profileVisibility** (string, optional) - Privacy setting
  - Values: 'public', 'private', 'followers_only'

### **User Preferences**
- [ ] **notificationPreferences** (object, optional)
  - [ ] weeklyDigest, newArticles, commentReactions, newInsightAlerts, followedAuthorUpdates
- [ ] **readingPreferences** (object, optional)
  - [ ] fontSize, fontType, backgroundColor, lineHeight
- [ ] **elementVisibility** (object, optional)
  - [ ] savedItems, followedTopics, contributions

### **User Statistics**
- [ ] **userStats** (object, optional)
  - [ ] articlesRead, insightsViewed, conceptsExplored, collectionsCompleted, commentsMade, libraryItemsCount
- [ ] **dateJoined** (ISO string, optional) - Registration date
- [ ] **lastLogin** (ISO string, optional) - Last login time

### **User Subscription Data**
- [ ] **subscriptionDetails** (object, optional)
  - [ ] type ('free', 'premium', 'enterprise')
  - [ ] status ('active', 'cancelled', 'expired', 'trial')
  - [ ] nextPaymentDate, renewalPeriod

### **Usage Context**
- **Authentication**: Core user fields for login state
- **Profile Page**: Full profile data including preferences
- **User Settings**: Preferences and subscription management
- **My Page**: Statistics and activity data

---

## **User Activity & Saved Items Data Requirements**

### **Saved Items Data**
- [ ] **savedItems** (SavedItem[]) - User's saved content
  - [ ] id, type ('article', 'insight', 'concept', 'collection')
  - [ ] Need to fetch full item details for display

### **Follow Relationships**
- [ ] **followedAuthors** (string[]) - IDs of followed authors
- [ ] **followedConcepts** (string[]) - IDs of followed concepts
- [ ] **followedInsights** (string[]) - IDs of followed insights
- [ ] **followedCollections** (string[]) - IDs of followed collections

### **Reading Progress**
- [ ] **readingProgress** (ReadingProgress[]) - Article reading progress
  - [ ] articleId, progressPercent, lastReadPosition, lastReadDate

### **Search History**
- [ ] **recentSearches** (string[]) - Recent search queries
- [ ] **searchPreferences** (object) - Search and filter preferences
  - [ ] contentType, dateRange, authors, concepts

### **Usage Context**
- **My Page**: Display all saved items with full details
- **Save/Follow Buttons**: Check and update user relationship status
- **Reading Progress**: Track and restore reading position
- **Search**: Populate recent searches and preferences

---

## **Comments & Engagement Data Requirements**

### **Comments Data**
- [ ] **comments** (Comment[]) - Article/insight comments
  - [ ] id, userId, userName, userAvatarUrl, text, timestamp
  - [ ] likesCount, isEdited, replies[], parentId
  - [ ] currentUserCanEdit, currentUserCanDelete

### **Reactions Data**
- [ ] **reactions** (Reaction[]) - User reactions to content
  - [ ] contentId, contentType, reactionType, userId, timestamp

### **Usage Context**
- **Article/Insight Detail Pages**: Display comments and reactions
- **User Engagement**: Track user interactions with content

---

## **Questions & Interactive Content Data Requirements**

### **Questions Data**
- [ ] **questions** (Question[]) - Interactive questions
  - [ ] id, questionText, answerFormat, options[], relatedTopicId
  - [ ] sourceType, sourceId, sourceTitle, sourceUrl

### **Question Options**
- [ ] **options** (QuestionOption[]) - Multiple choice options
  - [ ] id, text, isCorrect (for admin/validation)

### **User Answers**
- [ ] **userAnswers** (UserAnswer[]) - User question responses
  - [ ] questionId, userId, answer, timestamp

### **Usage Context**
- **Question Cards**: Display interactive questions
- **Progress Tracking**: Track user question completion
- **Analytics**: Measure engagement with interactive content

---

## **Search & Discovery Data Requirements**

### **Search Results Data**
- [ ] **searchResults** (SearchResult[]) - Search result aggregation
  - Mixed results from articles, insights, concepts, authors, collections
  - [ ] type, id, title, summary, url, relevanceScore, highlights

### **Filter Options Data**
- [ ] **filterOptions** (FilterOptions) - Available filters
  - [ ] types[], dateRanges[], organisations[], articleTypes[], fields[], interests[]
  - [ ] sortBy options with direction

### **Faceted Search Data**
- [ ] **facets** (Facet[]) - Search facets with counts
  - [ ] field, values[] with counts

### **Usage Context**
- **Search Page**: Display mixed search results with filtering
- **Explore Page**: Advanced filtering and discovery
- **Auto-suggestions**: Search completions and suggestions

---

## **Data Format Specifications**

### **Date Formats**
- All dates should be in **ISO 8601 format** (e.g., "2024-01-15T10:30:00Z")
- Frontend will handle timezone conversion and localization

### **HTML Content**
- **Rich content fields** (mainContent, narrative_output) should be sanitized HTML
- Support for basic formatting: headings, paragraphs, lists, links, emphasis

### **Image URLs**
- All image URLs should be **absolute URLs**
- Support for responsive images with multiple sizes preferred
- Fallback handling for missing images

### **Array Fields**
- **Empty arrays** should be returned as `[]`, not `null`
- **Consistent ordering** for preview arrays (e.g., by relevance, date)

### **Optional Fields**
- **Missing optional fields** should be returned as `null` or omitted
- **Boolean fields** should always have explicit values, not null

### **Pagination Format**
```typescript
{
  data: T[],
  meta: {
    total: number,
    page: number,
    per_page: number,
    page_count: number
  }
}
```

### **Error Responses**
```typescript
{
  error: {
    code: string,
    message: string,
    details?: object
  }
}
```

---

## **Performance & Caching Considerations**

### **Data Prefetching**
- **List pages**: Include preview relationships in single query
- **Detail pages**: Consider related content prefetching
- **Home page**: Optimize for multiple entity type aggregation

### **Field Selection**
- Support **sparse fieldsets** to minimize data transfer
- **Preview vs Detail** field selections for performance
- **Relationship depth** control to prevent over-fetching

### **Caching Headers**
- **Static content**: Long cache times (articles, insights)
- **User-specific data**: No cache or short cache times
- **Aggregated data**: Medium cache times with cache invalidation

---

## **Implementation Priority**

### **Phase 2A (High Priority)**
1. ✅ **Articles**: Core fields + basic relationships
2. ✅ **Concepts**: Core fields + statistics
3. ✅ **Insights**: Core fields + basic relationships
4. ✅ **Basic User Authentication**: Core user fields
5. ✅ **Saved Items**: Basic save/unsave functionality

### **Phase 2B (Lower Priority)**
1. **Complex Relationships**: Full related content data
2. **User Profiles**: Complete user preference system
3. **Comments & Engagement**: Full interaction system
4. **Search & Discovery**: Advanced filtering and faceted search
5. **Analytics & Progress**: Detailed user activity tracking

---

## **Validation Checklist**

Use this checklist to verify complete data coverage:

### **For Each Entity Type**
- [ ] All required fields defined in TypeScript interfaces
- [ ] User-specific data (saved, followed, progress) included
- [ ] Preview vs Detail field sets clearly defined
- [ ] Relationship data properly structured
- [ ] Error handling for missing/invalid data

### **For Each Page/Component**
- [ ] All displayed data fields identified
- [ ] Loading states account for async data
- [ ] Error states handle missing data gracefully
- [ ] User interactions (save, follow) have data endpoints
- [ ] Performance considerations documented

### **Cross-Entity Consistency**
- [ ] ID references consistent across entities
- [ ] Preview data structures match between entities
- [ ] User relationship patterns consistent
- [ ] Date/time formats standardized
- [ ] Error response formats consistent

This checklist ensures comprehensive coverage of all data requirements for the Directus integration, providing a clear roadmap for API development and frontend implementation.