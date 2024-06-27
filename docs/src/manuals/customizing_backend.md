# Customizing Backend


If you want to add a feature by modifying code, you need to follow these steps:

1. Modify db table (Migration)
2. Add a Model to API Structure (ORM)
3. Add or modify an API

Let's break this down step by step.


<hr/> 


In this project, the databse is managed directly through SQL migrations without ORM. We use [knex](https://knexjs.org/guide/schema-builder.html#alter) to manage queries. Let's create simple table (`Memo`) to see how it works.

## 1. Applying migration

The details of how to use **migration through knex** can be found [here](https://knexjs.org/guide/migrations.html). 

<br/>
To add a table to the database, migration file need to be created. Type this command to create migration file:

<br/>

```bash
pnpm mcreate create_memo
```

<br/>

A file named `{timestamp}_create_memo.js` will be created in the `migrations/` directory. Now, open this file and define following:

```js
const table = "memos";

exports.up = function (knex) {
  return knex.schema.createTable(table, function (t) {
    t.increments("id").primary();
    t.datetime("createdAt").defaultTo(knex.fn.now());
    t.datetime("updatedAt");

    t.integer("userId").references("users.id").onDelete("SET NULL").onUpdate("CASCADE");
    t.text("content").notNullable();
  });
};

exports.down = function (knex) {
  return knex.schema.dropTable(table);
};
```

Apply the above migration to the database with this command:

```bash
# stands for migrations:up, defined in package.json
pnpm mup
```

If you want to revert the applied migration, type this command.
```bash
# stands for migrations:down, defined in package.json
pnpm mdown
```


Then, check your database to confirm that the table named **memos** has been created. Now, Let's define the **Model** for **memos** at the code level.

<br/>

## 2. Define Model (ORM)

Simply copy and paste `src/models/_template` directory and rename it to `src/models/Memo`. Then open `src/models/Memo/schema.ts` file and define the following:

```ts
// src/models/Memo/schema.ts

import { z } from "zod";
import { baseModelSchema, insertFormSchema, getOptionSchema, listOptionSchema } from "../$commons/schema";
import { TG } from "@/utils/type_generator";


export const memoFormSchema = insertFormSchema.extend({
  userId: z.number(),
  content: z.string(),
});

export const memoSchema = baseModelSchema.extend(memoFormSchema.shape);

// config to define new types
TG.add(tgKey, "MemoFormT", memoFormSchema);
TG.add(tgKey, "MemoT", memoSchema);
```
<br/>


Once you define the schema, you can generate types based on the above schema automatically. Type this command to generate types.

```bash
pnpm gentype
```

Check that a file `src/types/Memo.ts` is created. This file contains the types of model that is used in Typescript.

Then open the file `src/models/Memo/model.ts` and define as below. `models.ts` file file functions as ORM.

```ts
// src/models/Memo/model.ts

import { DataModel } from "@/utils/orm";
import type { MemoFormT, MemoT } from "@/types/Model";


const table = "memos";
export const memoM = new DataModel<MemoFormT, MemoT>(table);
```

After completing all above processes, you can import the **Memo** model like you would use in any other ORM.

```ts
import { memoM } from '@/models/Memo';

async test() {
  const created = await memoM.create({
    userId: 1,
    content: 'sample test',
  })
  // Created Memo item to be created
  console.log(created) 

  const fetched = await memoM.findOne({ id: 1 });
  // Memo item fetched
  console.log(fetched)
}

test()
```

</br>



## 3. Add/Modify API

This project tries to design API following RESTful principle. Basic API structure is as follows:

```
(GET) {HOST}/memos/

Fetch a list of data from the "memo" table (List Data)

(GET) {HOST}/memos/:id

Fetch a specific item of data(by ID) from the "memo" table

(POST) {HOST}/momos/

Create an item in the "memo" table

(PUT) {HOST}/memos/

Modify multiple items in the "memo"a table

(PATH) {HOST}/memos/:id

Modify a specific item in the "memo" table

(DELETE) {HOST}/memos/:id

Delete a specific from the "memo" table
```


To see how the API is structured in this project, let’s create simple APIs for `List` and `Create`. First, open the file `src/models/schema.ts` and define the parameters for the API.



```ts
// src/models/Memo/schema.ts

... (model schema)

export const getMemoOptionSchema = getOptionSchema.extend({
}).partial();
export const listMemoOptionSchema = listOptionSchema.extend({
  ...getMemoOptionSchema.shape,
}).partial();


TG.add(tgKey, "GetMemoOptionT", getMemoOptionSchema);
TG.add(tgKey, "ListMemoOptionT", listMemoOptionSchema);
```

Then, create a type for the option by following command:

```bash
pnpm gentype
```

Verify that `src/types/Memo.ts` file has been updated with the new types `GetMemoOptionT` and `ListMemoOptionT`.

<br/>

Next, create a file `types/Memo.api.ts` and define types for the API as follows. This file will be used by frontend and used to send API to backend.

```ts
// types/Memo.api.ts

import { MemoT, MemoFormT, ListMemoOptionT } from "./Memo";

// (GET) /
export type ListRqs = ListMemoOptionT
export type ListRsp = ListData<MemoT>;

// (POST) /
export type CreateRqs = { form: MemoFormT }
export type CreateRsp = MemoT
```

Next, define `Controller` and `DTO` under the NestJS API structure. If you are not familiar with the API conventions of NestJS, please check [this guide](https://docs.nestjs.com)

```ts
// apis/Memo/dto.ts

import { createZodDto } from "nestjs-zod";
import { z } from "nestjs-zod/z";
import { memoFormSchema, listMemoOptionSchema } from "@/models/Memo";
// import { } from "@/types/_";

// create
export class CreateMemoDto extends createZodDto(z.object({ form: memoFormSchema }))

// list
export class ListMemoDto extends createZodDto(listInvoiceOptionSchema) {}
```

Define `Controller`:

```ts
// apis/Memo/controller.ts

import {
  Controller, Post, Get,
  Body, Param, Query,
} from "@nestjs/common";
import {
  ListMemoDto,
  CreateMemoDto,
} from "./dtos";
import type * as R from "@/types/Memo.api";
import { MemoService } from "./service";


@Controller("memos")
export class MemoController {
  constructor(private readonly service: MemoService) {}

  @Get("/")
  async list(
    @Query() query: ListMemoDto,
  ): Promise<R.ListRsp> {
    const listOpt = query satisfies R.ListRqs;
    return await this.service.list(listOpt);
  }

  @Post('/')
  async create(
    @Body() body: CreateMemoDto,
  ): Promise<R.CreateRsp> {
    const { form } = body satisfies R.CreateRqs;
    return await this.service.create(form);
  }
}
```


Next, define the logic for the service (`list`, `create`, etc.) in service.ts. Below is a simplified example of the logic that goes into service.ts.


```ts
// apis/Memo/service.ts

import { Injectable } from "@nestjs/common";
import * as err from "@/errors";
import { memoM } from "@/models/Memo";
import { MemoT, MemoFormT, ListMemoOptionT } from "@/types";

@Injectable()
export class MemoService {
  constructor() {}

  async create(form: MemoFormT): Promise<InvoiceT> {
    const created = await memoM.create(form);
    if (!created) {
      throw new err.NotAppliedE();
    }
    return created;
  }

  async list(listOpt: ListMemoOptionT): Promise<ListData<MemoT>> {
    const fetched = await memoM.findMany({});
    return { data: [], nextCursor: null };
  }
}
```

Then, define `module.ts`:

```ts
import { Module } from "@nestjs/common";
import { MemoController } from "./controller";
import { MemoService } from "./service";

@Module({
  controllers: [MemoController],
  providers: [MemoService],
})
export class MemoModule {}
```
You can now use the defined API after importing the above `module.ts` file in the `src/apis/app.module.ts` file.




<hr/>

### Additional Details
Following rules are important in this project.

> 1. Files defined in `types/` are passed to frontend and utilized. Types for model and api option can be generated with `pnpm gentype`.
> 2. Types for API, which is defined in `types/memo.api.ts`, should be matched with body or query params by `satisfies` keyword. This can prevent type mismatch caused by human error.

